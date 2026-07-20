"""Shop master-data lookups, availability windows, and paying for things.

The four shops the routes serve all share the same shape -- an entry names what you get
(``thing_*``) and what it costs (``required_*``) -- but each keeps that in its own master
table and tracks its limits in its own per-user table:

- **exchange shop**: ExchangeShopMaster.lineup[] (ExchangeShopThing), limits in
  ``exchange_limit``, which resets per the entry's ShopReplaceTypes period.
- **market**: MarketFrameThingMaster, rolled per user into ``market_thing``.
- **permanent market**: PermanentMarketThingMaster, lifetime limits in
  ``permanent_market_thing``.
- **jewel shop**: JewelShopItemMaster, real-money packs, counted in ``jewel_shop``.
"""

import random
from datetime import datetime, timedelta, timezone
from typing import Optional

from db.user import add_currency, get_currencys, get_items, increment_item_stock
from helpers.cache import cache
from models.enums import ShopReplaceTypes, ThingTypes

# jewels for each successive manual market refresh within one day. Ten entries because ten
# is the daily ceiling -- past that the market cannot be refreshed again until reset.
MARKET_REFRESH_COSTS = (10, 20, 30, 30, 30, 50, 50, 50, 50, 50)
MARKET_MAX_REFRESHES = len(MARKET_REFRESH_COSTS)

# The market turns over twice a day, at 11:00 and 23:00 JST. Everything about it resets on
# that one boundary: new frames, every hasPurchased cleared, and the paid-refresh count back
# to zero -- so the ten refreshes above are ten per *period*, twice a day, not ten per day.
# Note this is the market's own clock, unrelated to the 05:00 JST daily reset that
# helpers/daily.py restores daily allowances on.
MARKET_RESET_HOURS = (11, 23)
_JST = timezone(timedelta(hours=9))

# TODO: guessed. Frames 4 and 11 of the one captured market each carried a flat 10%, the
# other 13 none, so a per-frame chance of a fixed 10% matches what was seen -- but the real
# trigger (a rarity/display_type weighting? a daily promo?) is unknown, as is whether any
# rate other than 10 exists.
MARKET_DISCOUNT_PERCENT = 10
MARKET_DISCOUNT_CHANCE = 2 / 15

# Unlocking a song costs 10 tickets; buying one song's Olivier chart costs 1. Both are
# fixed prices with no master row behind them -- ExchangeShopMaster has no category 6
# (Music) entry at all, so nothing in masterdata prices either one.
MUSIC_UNLOCK_ITEM_ID = 130001
MUSIC_UNLOCK_COST = 10
MUSIC_SCORE_ITEM_ID = 130001
MUSIC_SCORE_COST = 1

_EXCHANGE_THINGS: dict = {}  # ExchangeShopThing.id -> (shop master, thing)
_MARKET_FRAMES: dict = {}
_MARKET_POOLS: dict = {}  # frame number -> [MarketFrameThingMaster ids]
_PERMANENT: dict = {}
_JEWEL_ITEMS: dict = {}
_LIVE_MUSIC: dict = {}  # LiveMaster.id -> music_master_id


def _build() -> None:
    if _EXCHANGE_THINGS:
        return
    for shop in cache.exchange_shop_master:
        for thing in shop.lineup or []:
            _EXCHANGE_THINGS[thing.id_] = (shop, thing)
    _MARKET_FRAMES.update({f.id_: f for f in cache.market_frame_thing_master})
    # a frame's candidates are encoded in the master id: id // 100 is the frame it can
    # appear in, id % 100 the variant. The 138 rows fall into exactly 15 such groups, and
    # every id in the captured market sits in the group matching its own frame_number.
    for master_id in _MARKET_FRAMES:
        _MARKET_POOLS.setdefault(master_id // 100, []).append(master_id)
    _PERMANENT.update({p.id_: p for p in cache.permanent_market_thing_master})
    _JEWEL_ITEMS.update({j.id_: j for j in cache.jewel_shop_item_master})


def available(start_date, end_date, now: Optional[datetime] = None) -> bool:
    """Whether ``now`` falls inside a master row's sale window.

    A row whose dates are missing or unparseable counts as available -- an absent window is
    read as "no restriction" rather than "never on sale". Note that the ``0001-01-01``
    sentinel some rows carry parses fine and so reads as *closed*, which is deliberate: it
    marks an entry that was never given a real window. It affects 129 of the 1926
    JewelShopItemMaster rows and nothing in the exchange or permanent-market masters.
    """
    at = now or datetime.now(timezone.utc)
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except (TypeError, ValueError):
        return True
    return start <= at <= end


def exchange_shop_thing(m_exchange_shop_thing_id: int):
    """``(ExchangeShopMaster, ExchangeShopThing)`` for one lineup entry, or ``(None, None)``.

    Entries are addressed by their own id with no shop id alongside, so the reverse index is
    what lets a route find the shop an exchange belongs to.
    """
    _build()
    return _EXCHANGE_THINGS.get(m_exchange_shop_thing_id, (None, None))


def market_frame(market_frame_thing_master_id: int):
    _build()
    return _MARKET_FRAMES.get(market_frame_thing_master_id)


def permanent_market_thing(permanent_market_thing_master_id: int):
    _build()
    return _PERMANENT.get(permanent_market_thing_master_id)


def jewel_shop_item(m_jewel_shop_item_id: int):
    _build()
    return _JEWEL_ITEMS.get(m_jewel_shop_item_id)


def live_music_master_id(live_master_id: int) -> Optional[int]:
    """The song a live (one chart of one song) belongs to, or None.

    ExchangeMusicScore is addressed by live id but the purchase it records lives on the
    music row, so the chart has to be resolved back to its song first.
    """
    _build()
    return _LIVE_MUSIC.get(live_master_id)


def roll_market() -> list[tuple[int, int, Optional[int]]]:
    """Roll a fresh market as ``(frame_number, master_id, discount_percent)`` frames.

    Always the full 15 frames, one drawn per frame from that frame's own pool -- the frames
    are fixed slots, not a sample of a shared pool, so frame 3 can only ever hold a 3xx
    entry. Pool sizes vary a lot (frame 2 has 2 candidates, frame 13 has 21).

    TODO: unweighted within a pool. MarketFrameThingMaster carries a MarketDisplayTypes
    (Default / Recommend / Rare) that plausibly skews the draw; one capture can't show it.
    """
    _build()
    frames: list[tuple[int, int, Optional[int]]] = []
    for frame_number in sorted(_MARKET_POOLS):
        master_id = random.choice(_MARKET_POOLS[frame_number])
        discount = (
            MARKET_DISCOUNT_PERCENT
            if random.random() < MARKET_DISCOUNT_CHANCE
            else None
        )
        frames.append((frame_number, master_id, discount))
    return frames


def _most_recent(now_micros: int, hours) -> int:
    """Epoch-micros of the latest of today's ``hours`` (JST) at or before ``now``, falling
    back to the last of them yesterday when ``now`` precedes all of today's."""
    now = datetime.fromtimestamp(now_micros / 1_000_000, _JST)
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    boundaries = [midnight + timedelta(hours=h) for h in sorted(hours)]
    passed = [b for b in boundaries if b <= now]
    latest = passed[-1] if passed else boundaries[-1] - timedelta(days=1)
    return int(latest.timestamp() * 1_000_000)


def market_reset(now_micros: int) -> int:
    """Epoch-micros of the most recent market turnover (11:00 / 23:00 JST).

    A market stamped before this belongs to the previous period, so it gets fresh frames,
    every ``hasPurchased`` cleared, and its paid-refresh count zeroed.
    """
    return _most_recent(now_micros, MARKET_RESET_HOURS)


def refresh_cost(refresh_times: int) -> Optional[int]:
    """Jewels for the next manual refresh, given how many have already been bought in the
    current market period, or None once the ceiling is reached. None is what the client is
    told when the button is spent -- ``required_jewel_for_refresh`` is nullable for this."""
    index = max(int(refresh_times), 0)
    if index >= MARKET_MAX_REFRESHES:
        return None
    return MARKET_REFRESH_COSTS[index]


def period_until(
    replace_type: Optional[int], now: Optional[datetime] = None
) -> Optional[int]:
    """When the current limit period ends, in epoch microseconds, or None for a lifetime cap.

    An exchange_limit row stores this as ``until``; once it passes, the entry's count resets.
    Daily rolls over at midnight UTC, Weekly on the following Monday, Monthly on the 1st.

    TODO: the game's day boundary is very likely JST (05:00 local, as elsewhere in this
    server), not UTC midnight. Left UTC until a capture shows a real ``until`` to match.
    """
    if replace_type is None:
        return None
    try:
        kind = ShopReplaceTypes(int(replace_type))
    except ValueError:
        return None
    at = now or datetime.now(timezone.utc)
    midnight = at.replace(hour=0, minute=0, second=0, microsecond=0)
    if kind == ShopReplaceTypes.Daily:
        end = midnight + timedelta(days=1)
    elif kind == ShopReplaceTypes.Weekly:
        end = midnight + timedelta(days=7 - at.weekday())
    elif kind == ShopReplaceTypes.Monthly:
        end = (midnight.replace(day=1) + timedelta(days=32)).replace(day=1)
    else:
        return None  # None_ / DailyPassExpired never roll over on a clock
    return int(end.timestamp() * 1_000_000)


async def charge(
    conn, user_id: int, thing_type: int, thing_id: int, quantity: int
) -> Optional[set]:
    """Take payment for one purchase.

    Returns the present-entity names the charge touched -- so the caller can report the
    balance going down -- or None, *having written nothing*, when the caller can't afford
    it. Every shop route checks for None and rejects before granting, so a failed charge can
    never hand out the goods.
    """
    if quantity <= 0:
        return set()
    try:
        kind = ThingTypes(int(thing_type))
    except ValueError:
        return None

    if kind in (ThingTypes.Coin, ThingTypes.Jewel):
        currency = next(iter(await conn.fetch(get_currencys(user_id))), None)
        if currency is None:
            return None
        if kind == ThingTypes.Coin:
            if currency.coin < quantity:
                return None
            await conn.execute(add_currency(user_id, coin=-quantity))
        else:
            # TODO: paid and free jewels are separate balances and only freeJewel is spent
            # here, matching the same shortcut _spend_cost() takes in routes/gachas.py.
            if currency.freeJewel < quantity:
                return None
            await conn.execute(add_currency(user_id, free_jewel=-quantity))
        return {"Currency"}

    if kind == ThingTypes.Item:
        row = next(
            (
                i
                for i in await conn.fetch(get_items(user_id))
                if i.itemMasterId == thing_id
            ),
            None,
        )
        if row is None or row.stock < quantity:
            return None
        await conn.execute(increment_item_stock(user_id, thing_id, -quantity))
        return {"Item"}

    # nothing else is ever priced in a captured shop entry -- every required_thing_type seen
    # is Item, Coin or Jewel. Refuse rather than silently letting a purchase through free.
    return None
