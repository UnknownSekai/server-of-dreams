import random
import time
from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from db.user import (
    consume_exchange_limit,
    consume_market_refresh,
    consume_permanent_market_limit,
    get_market_things,
    get_markets,
    get_musics,
    purchase_market_thing,
    record_jewel_shop_purchase,
    release_music_olivier,
    replace_market_things,
    roll_over_market,
    touch_viewed_shop,
)
from helpers.msgpack import fault, read_request, respond
from helpers.music_unlock import apply_unlocks
from helpers.shops import (
    MARKET_MAX_REFRESHES,
    MUSIC_SCORE_COST,
    MUSIC_SCORE_ITEM_ID,
    MUSIC_UNLOCK_COST,
    MUSIC_UNLOCK_ITEM_ID,
    available,
    charge,
    exchange_shop_thing,
    jewel_shop_item,
    live_music_master_id,
    market_frame,
    market_reset,
    permanent_market_thing,
    period_until,
    refresh_cost,
    roll_market,
)
from helpers.things import grant_thing, grant_things_consolidated, present_type
from helpers.user_data import build_present, current_user_id
from models import *

router = APIRouter(tags=["Shops"])


def _random_id() -> int:
    return random.randint(1_000_000, 9_999_999_999)


def _now() -> int:
    return int(time.time() * 1_000_000)


class _Rejected(Exception):
    """A purchase that cannot go through, raised rather than returned so it unwinds the
    enclosing ``conn.transaction()``.

    This has to be an exception: a purchase writes in stages (count the limit, charge, then
    grant) and a plain ``return`` out of an ``async with conn.transaction()`` block leaves
    the context manager without an error, which *commits* the partial write. Rejecting a
    purchase after its exchange limit was already counted would burn the slot and hand back
    nothing. Raising rolls the whole attempt back.
    """

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


async def _exchange(conn, user_id: int, thing, quantity: int, now: int):
    """Run one exchange-shop purchase: count it against the cap, charge, grant.

    Returns ``(received_things, refreshed_entity_names)``, or raises :class:`_Rejected`.
    Ordered so nothing is granted unless payment succeeded and nothing is charged unless
    the exchange limit had room.
    """
    limit = thing.exchange_limit
    if limit is not None:
        row = await conn.fetchrow(
            consume_exchange_limit(
                user_id,
                thing.id_,
                quantity,
                limit,
                int(thing.replace_type or 0),
                period_until(thing.replace_type),
                now,
                _random_id(),
            )
        )
        if row is None:
            raise _Rejected("ExchangeLimitExceeded")

    spent = await charge(
        conn,
        user_id,
        int(ThingTypes.Item),
        thing.required_item_master_id,
        (thing.required_quantity or 0) * quantity,
    )
    if spent is None:
        raise _Rejected("NotEnoughThing")

    received = await grant_things_consolidated(
        conn,
        user_id,
        [
            (
                int(thing.thing_type),
                thing.thing_id,
                (thing.thing_quantity or 1) * quantity,
            )
        ],
    )
    refresh = set(spent) | {present_type(int(r.type)) for r in received}
    if limit is not None:
        refresh.add("ExchangeLimit")
    refresh.discard(None)
    return received, refresh


async def _market_state(conn, user_id: int, now: int):
    """The caller's current market, rolling a new one if the period turned over.

    Returns ``(MarketThing rows, refresh_times)``. The lineup is stored rather than
    regenerated per call, so a reconnect shows the same 15 frames -- and so ``has_purchased``
    survives, which is the whole point of keeping it.
    """
    rolled = await conn.fetchrow(
        roll_over_market(user_id, now, _random_id(), market_reset(now))
    )
    if rolled is not None:
        # first look since 11:00 or 23:00 JST (or ever): fresh frames, purchases cleared,
        # and the refresh count zeroed with them
        await conn.execute(replace_market_things(user_id, roll_market()))
        return await conn.fetch(get_market_things(user_id)), 0

    market = next(iter(await conn.fetch(get_markets(user_id))), None)
    refresh_times = market.refreshTimes if market is not None else 0
    return await conn.fetch(get_market_things(user_id)), refresh_times


def _market_result(rows, refresh_times: int) -> MarketResult:
    # required_jewel_for_refresh is None once the period's ten refreshes are spent
    return MarketResult(
        things=[
            MarketThing(
                frame_number=r.frameNumber,
                market_frame_thing_master_id=r.marketFrameThingMasterId,
                has_purchased=r.hasPurchased,
                discount_percent=r.discountPercent,
            )
            for r in rows
        ],
        required_jewel_for_refresh=refresh_cost(refresh_times),
    )


async def _buy_market_frame(conn, user_id: int, frame_number: int):
    """Buy one rolled market frame. ``(received, refreshed)``, or raises :class:`_Rejected`."""
    claimed = await conn.fetchrow(purchase_market_thing(user_id, frame_number))
    if claimed is None:
        # either no such frame, or somebody already bought it -- the UPDATE distinguishes
        # neither, and both mean the same thing to the client
        raise _Rejected("AlreadyPurchased")

    frame = market_frame(claimed.marketFrameThingMasterId)
    if frame is None:
        raise _Rejected("InvalidRequest")

    price = frame.required_thing_quantity or 0
    if claimed.discountPercent:
        price = price * (100 - claimed.discountPercent) // 100
    spent = await charge(
        conn, user_id, int(frame.required_thing_type), frame.required_thing_id, price
    )
    if spent is None:
        raise _Rejected("NotEnoughThing")

    received = await grant_things_consolidated(
        conn,
        user_id,
        [(int(frame.thing_type), frame.thing_id, frame.thing_quantity or 1)],
    )
    refresh = set(spent) | {present_type(int(r.type)) for r in received}
    refresh.discard(None)
    return received, refresh


# /api/Shops/ExchangeMarketThing/{number}
@router.post(
    "/api/Shops/ExchangeMarketThing/{number}", name="Shops_ExchangeMarketThing"
)
async def shops_exchange_market_thing(request: Request, number: int):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payload = {}  # no payload -- the frame number is the path segment
    if user_id is None:
        return respond([])

    try:
        async with app.acquire_db() as conn:
            async with conn.transaction():
                received, refresh = await _buy_market_frame(conn, user_id, number)
    except _Rejected as rejected:
        return respond([], faults=[fault(rejected.code)])

    present = await build_present(app, user_id, *sorted(refresh))
    return respond(received, present=present)


# /api/Shops/ExchangeMarketThings
@router.post("/api/Shops/ExchangeMarketThings", name="Shops_ExchangeMarketThings")
async def shops_exchange_market_things(request: Request):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payload = await read_request(request)
    if user_id is None:
        return respond([])

    # a bare list of frame numbers, e.g. [8, 9] -- confirmed by capture
    frames = payload if isinstance(payload, list) else []
    received: list = []
    refresh: set = set()
    try:
        async with app.acquire_db() as conn:
            # one transaction for the whole batch: if the third frame is unaffordable the
            # first two are rolled back too, rather than half-buying the request
            async with conn.transaction():
                for number in frames:
                    got, meta = await _buy_market_frame(conn, user_id, int(number))
                    received.extend(got)
                    refresh |= meta
    except _Rejected as rejected:
        return respond([], faults=[fault(rejected.code)])

    present = await build_present(app, user_id, *sorted(refresh)) if refresh else []
    return respond(received, present=present)


# /api/Shops/ExchangeMusic/{mMusicId}
@router.post("/api/Shops/ExchangeMusic/{mMusicId}", name="Shops_ExchangeMusic")
async def shops_exchange_music(request: Request, mMusicId: int):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payload = {}  # no payload -- the music is the path segment
    if user_id is None:
        return respond(ReceivedThing())

    try:
        async with app.acquire_db() as conn:
            async with conn.transaction():
                owned = next(
                    (
                        m
                        for m in await conn.fetch(get_musics(user_id))
                        if m.musicMasterId == mMusicId and m.isPossession
                    ),
                    None,
                )
                if owned is not None:
                    raise _Rejected("AlreadyPurchased")

                spent = await charge(
                    conn,
                    user_id,
                    int(ThingTypes.Item),
                    MUSIC_UNLOCK_ITEM_ID,
                    MUSIC_UNLOCK_COST,
                )
                if spent is None:
                    raise _Rejected("NotEnoughThing")

                received = await grant_thing(
                    conn, user_id, int(ThingTypes.Music), mMusicId, 1
                )
    except _Rejected as rejected:
        return respond(ReceivedThing(), faults=[fault(rejected.code)])

    present = await build_present(app, user_id, *sorted(set(spent) | {"Music"}))
    return respond(received, present=present)


# /api/Shops/ExchangeMusicScore/{mLiveId}
@router.post("/api/Shops/ExchangeMusicScore/{mLiveId}", name="Shops_ExchangeMusicScore")
async def shops_exchange_music_score(request: Request, mLiveId: int):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payload = {}  # no payload -- the live is the path segment
    # buys the Olivier chart of the song this live belongs to. Only a chart the user has
    # already made Purchasable (its level within what they've cleared -- see
    # helpers/music_unlock) can be bought; the guard lives in release_music_olivier.
    music_master_id = live_music_master_id(mLiveId)
    if user_id is None or music_master_id is None:
        return respond(BooleanResult())

    try:
        async with app.acquire_db() as conn:
            async with conn.transaction():
                released = await conn.fetchrow(
                    release_music_olivier(
                        user_id,
                        music_master_id,
                        int(OlivierReleaseStatuses.Purchasable),
                        int(OlivierReleaseStatuses.Released),
                    )
                )
                if released is None:
                    # not owned, not yet purchasable, or already bought
                    raise _Rejected("InvalidRequest")

                spent = await charge(
                    conn,
                    user_id,
                    int(ThingTypes.Item),
                    MUSIC_SCORE_ITEM_ID,
                    MUSIC_SCORE_COST,
                )
                if spent is None:
                    raise _Rejected("NotEnoughThing")

                # the 20th Olivier bought opens every owned song's Stella (see
                # helpers/music_unlock); the whole Music list is rebuilt below either way
                await apply_unlocks(conn, user_id)
    except _Rejected as rejected:
        return respond(BooleanResult(), faults=[fault(rejected.code)])

    present = await build_present(app, user_id, *sorted(set(spent) | {"Music"}))
    return respond(BooleanResult(is_success=True), present=present)


# /api/Shops/ExchangePermanentMarketThing/{PermanentMarketThingMasterid}?permanentMarketThingMasterId=&quantity=
@router.post(
    "/api/Shops/ExchangePermanentMarketThing/{PermanentMarketThingMasterid}",
    name="Shops_ExchangePermanentMarketThings",
)
async def shops_exchange_permanent_market_things(
    request: Request,
    PermanentMarketThingMasterid: int,
    permanentMarketThingMasterId: Optional[int] = None,
    quantity: Optional[int] = None,
):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payload = {}  # no payload -- the entry is the path segment, the count a query param
    # the route carries the same master id twice, in the path and the query; they agree in
    # every capture, and the path segment is authoritative here
    master_id = PermanentMarketThingMasterid or permanentMarketThingMasterId
    count = max(1, int(quantity or 1))
    entry = permanent_market_thing(master_id) if master_id is not None else None
    if user_id is None or entry is None:
        return respond([])
    if not available(entry.start_date, entry.end_date):
        return respond([], faults=[fault("OutOfPeriod")])

    try:
        async with app.acquire_db() as conn:
            async with conn.transaction():
                if entry.exchange_limit is not None:
                    row = await conn.fetchrow(
                        consume_permanent_market_limit(
                            user_id, entry.id_, count, entry.exchange_limit
                        )
                    )
                    if row is None:
                        raise _Rejected("ExchangeLimitExceeded")

                spent = await charge(
                    conn,
                    user_id,
                    int(entry.required_thing_type),
                    entry.required_thing_id,
                    (entry.required_thing_quantity or 0) * count,
                )
                if spent is None:
                    raise _Rejected("NotEnoughThing")

                received = await grant_things_consolidated(
                    conn,
                    user_id,
                    [
                        (
                            int(entry.thing_type),
                            entry.thing_id,
                            (entry.thing_quantity or 1) * count,
                        )
                    ],
                )
    except _Rejected as rejected:
        return respond([], faults=[fault(rejected.code)])

    refresh = set(spent) | {present_type(int(r.type)) for r in received}
    if entry.exchange_limit is not None:
        refresh.add("PermanentMarketThing")
    refresh.discard(None)
    present = await build_present(app, user_id, *sorted(refresh))
    return respond(received, present=present)


# /api/Shops/ExchangeShopThing/{mExchangeShopThingId}/{quantity}
@router.post(
    "/api/Shops/ExchangeShopThing/{mExchangeShopThingId}/{quantity}",
    name="Shops_ExchangeShopThing",
)
async def shops_exchange_shop_thing(
    request: Request, mExchangeShopThingId: int, quantity: int
):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payload = {}  # no payload -- entry and count are both path segments
    shop, thing = exchange_shop_thing(mExchangeShopThingId)
    count = max(1, int(quantity or 1))
    if user_id is None or thing is None:
        return respond([])
    if not available(thing.start_date, thing.end_date) or not available(
        shop.start_date, shop.end_date
    ):
        return respond([], faults=[fault("OutOfPeriod")])

    now = _now()
    try:
        async with app.acquire_db() as conn:
            async with conn.transaction():
                received, meta = await _exchange(conn, user_id, thing, count, now)
    except _Rejected as rejected:
        return respond([], faults=[fault(rejected.code)])

    present = await build_present(app, user_id, *sorted(meta))
    return respond(received, present=present)


# /api/Shops/ExchangeShopThings
@router.post("/api/Shops/ExchangeShopThings", name="Shops_ExchangeShopThings")
async def shops_exchange_shop_things(request: Request):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payload = await read_request(request, ExchangeShopThingPayload)
    if user_id is None or payload is None:
        return respond([])

    # TODO: the singular payload here is what read_request already decoded before this route
    # was implemented, so this is treated as a one-entry batch. If the real endpoint takes a
    # list of ExchangeShopThingPayload, this needs the model changed to match -- capture
    # pending.
    shop, thing = exchange_shop_thing(payload.m_exchange_shop_thing_id)
    if thing is None:
        return respond([])
    if not available(thing.start_date, thing.end_date) or not available(
        shop.start_date, shop.end_date
    ):
        return respond([], faults=[fault("OutOfPeriod")])

    now = _now()
    try:
        async with app.acquire_db() as conn:
            async with conn.transaction():
                received, meta = await _exchange(
                    conn, user_id, thing, max(1, payload.quantity or 1), now
                )
    except _Rejected as rejected:
        return respond([], faults=[fault(rejected.code)])

    present = await build_present(app, user_id, *sorted(meta))
    return respond(received, present=present)


# /api/Shops/GetOrRefreshMarket
@router.post("/api/Shops/GetOrRefreshMarket", name="Shops_GetOrRefreshMarket")
async def shops_get_or_refresh_market(request: Request):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payload = {}  # no payload
    if user_id is None:
        return respond(MarketResult())

    now = _now()
    async with app.acquire_db() as conn:
        async with conn.transaction():
            rows, refresh_times = await _market_state(conn, user_id, now)
    return respond(_market_result(rows, refresh_times))


# /api/Shops/Purchase
@router.post("/api/Shops/Purchase", name="Shops_Purchase")
async def shops_purchase(request: Request):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payload = await read_request(request, PurchaseItemPayload)
    if user_id is None or payload is None:
        return respond([])

    item = jewel_shop_item(payload.m_jewel_shop_item_id)
    if item is None:
        return respond([])
    if not available(item.start_date, item.end_date):
        return respond([], faults=[fault("OutOfPeriod")])

    # NOTE: this grants the pack outright. These are real-money IAPs and the actual store
    # receipt is validated by the KmsGeneralPayment routes, not here -- on a private server
    # there is no receipt to check, so the purchase is simply honoured.
    #
    # TODO: the pack's give_paid_jewel lands in freeJewel, not the paidJewel column that
    # exists right beside it, because ThingTypes.Jewel maps to free in grant_thing() and
    # add_currency() takes no paid argument. Correcting it means teaching both about paid
    # jewels -- the same split routes/gachas.py punts on when charging for a roll.
    async with app.acquire_db() as conn:
        async with conn.transaction():
            received = await grant_things_consolidated(
                conn,
                user_id,
                [(int(ThingTypes.Jewel), 0, item.give_paid_jewel or 0)],
            )
            await conn.execute(
                record_jewel_shop_purchase(user_id, item.id_, _random_id(), None)
            )

    refresh = {present_type(int(r.type)) for r in received}
    refresh.add("JewelShop")
    refresh.discard(None)
    present = await build_present(app, user_id, *sorted(refresh))
    return respond(received, present=present)


# /api/Shops/UpdateLastViewedAt
@router.post("/api/Shops/UpdateLastViewedAt", name="Shops_UpdateLastViewedAt")
async def shops_update_last_viewed_at(request: Request):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payload = await read_request(request, UpdateLastViewedAtPayload)
    if user_id is None or payload is None:
        return respond(BooleanResult())

    async with app.acquire_db() as conn:
        await conn.execute(
            touch_viewed_shop(
                user_id,
                int(payload.viewed_shop_category_types),
                payload.exchange_shop_master_id,
                _now(),
                _random_id(),
            )
        )
    present = await build_present(app, user_id, "ViewedShop")
    return respond(BooleanResult(is_success=True), present=present)


# /api/Shops/RefreshMarketWithJewel
@router.post("/api/Shops/RefreshMarketWithJewel", name="Shops_UpdateMarketWithJewel")
async def shops_update_market_with_jewel(request: Request):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payload = {}  # no payload
    if user_id is None:
        return respond(MarketResult())

    now = _now()
    try:
        async with app.acquire_db() as conn:
            async with conn.transaction():
                # claim the refresh slot first: it both enforces the per-period ceiling and
                # tells us which step of the price curve this refresh is. Charging first
                # would mean pricing off a count that a concurrent refresh could move.
                claimed = await conn.fetchrow(
                    consume_market_refresh(
                        user_id,
                        now,
                        _random_id(),
                        market_reset(now),
                        MARKET_MAX_REFRESHES,
                    )
                )
                if claimed is None:
                    raise _Rejected("RefreshLimitExceeded")

                refresh_times = claimed.refreshTimes
                # the claim already counted this one, so the price is the step it just took
                price = refresh_cost(refresh_times - 1)
                spent = await charge(
                    conn, user_id, int(ThingTypes.Jewel), 0, price or 0
                )
                if spent is None:
                    raise _Rejected("NotEnoughThing")

                await conn.execute(replace_market_things(user_id, roll_market()))
                rows = await conn.fetch(get_market_things(user_id))
    except _Rejected as rejected:
        return respond(MarketResult(), faults=[fault(rejected.code)])

    present = await build_present(app, user_id, "Currency", "Market")
    return respond(_market_result(rows, refresh_times), present=present)


# /api/Shops/ViewPage
@router.post("/api/Shops/ViewPage", name="Shops_ViewPage")
async def shops_view_page(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    # TODO: unimplemented. Returns ConvertedThingResult[] (exchange_shop_master_id,
    # original_quantity, received_thing), but nothing in master data says what triggers a
    # conversion -- an empty list is the safe stand-in. Blocked on a capture.
    return respond(ViewShopResult())
