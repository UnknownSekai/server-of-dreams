import random
import time
from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from db.user import (
    add_currency,
    add_gacha_historys,
    add_gacha_rolls,
    breakthrough_poster,
    get_characters,
    get_currencys,
    get_gacha_historys,
    get_gacha_selected_things,
    get_items,
    get_posters,
    increment_item_stock,
    set_gacha_selected_things,
)
from helpers.cache import cache
from helpers.gacha import (
    active_gacha_ids,
    detail_of,
    dupe_conversion,
    emission_flags,
    lineup,
    piece_bonus,
    poster_max_phase,
    roll_limits,
    roll_prizes,
)
from helpers.msgpack import fault, read_request, respond
from helpers.things import grant_thing, grant_things_consolidated, present_type
from helpers.user_data import build_present, current_user_id
from models import *

router = APIRouter(tags=["Gachas"])

_GACHA_MASTER: dict = {}
_SELECTION_MASTER: dict = {}


def _random_gacha_id() -> int:
    return random.randint(1_000_000, 9_999_999_999)


async def _spend_cost(conn, user_id: int, detail) -> Optional[set]:
    """Charge a roll. Returns the present-entity names the charge touched, or None -- having
    written nothing -- when the caller cannot afford it, so the roll is rejected rather than
    given away.

    The spent balance has to reach present in its own right: a pull awarding only characters
    still has to show the jewels going down, and a capture of a 3000-jewel pull does return a
    Currency entry next to the characters.
    """
    if detail.is_free:
        return set()

    ticket_id = detail.required_ticket_m_item_id
    ticket_qty = detail.required_ticket_quantity or 0
    if ticket_id and ticket_qty:
        row = next(
            (
                i
                for i in await conn.fetch(get_items(user_id))
                if i.itemMasterId == ticket_id
            ),
            None,
        )
        if row is None or row.stock < ticket_qty:
            return None
        await conn.execute(increment_item_stock(user_id, ticket_id, -ticket_qty))
        return {"Item"}

    # TODO: paid and free jewels are separate balances and the client picks which a button
    # spends; both are charged against freeJewel here because no captured roll is priced in
    # paid jewels, leaving that path unobserved. The free-jewel path IS confirmed.
    jewels = (detail.free_jewel_amount or 0) + (detail.paid_jewel_amount or 0)
    if jewels:
        currency = next(iter(await conn.fetch(get_currencys(user_id))), None)
        if currency is None or currency.freeJewel < jewels:
            return None
        await conn.execute(add_currency(user_id, free_jewel=-jewels))
        return {"Currency"}
    return set()


async def _award_prize(conn, user_id: int, gacha, thing) -> list:
    """Hand over one prize, returning its ReceivedThing[].

    Three outcomes, in order:

    - you don't own it -> you get the character/poster itself.
    - you own a poster that isn't maxed -> it breaks through one phase instead of stacking,
      and the result reports the phase reached. The first pull creates it at phase 0 and the
      next four each advance one, so the 5th acquisition maxes it at phase 4.
    - anything else (a character dupe, or the 6th+ copy of a poster) -> it converts, and the
      conversion is what lands in received_things instead of the possession.

    One captured ten-pull shows two of these on the same rarity: SR 220070 (maxed) paid out
    frames while SR 220150 (at phase 2) came back as a Poster with after_phase=3.
    """
    thing_type = int(thing.thing_type)
    quantity = thing.thing_quantity or 1
    owns = False

    if thing_type == int(ThingTypes.Poster):
        owned = next(
            (
                p
                for p in await conn.fetch(get_posters(user_id))
                if p.posterMasterId == thing.thing_id
            ),
            None,
        )
        max_phase = poster_max_phase(thing.thing_id)
        if owned is not None and owned.breakthroughPhase < max_phase:
            await conn.execute(breakthrough_poster(user_id, owned.id, max_phase))
            return [
                ReceivedThing(
                    type=thing_type,
                    id_=thing.thing_id,
                    quantity=quantity,
                    after_phase=owned.breakthroughPhase + 1,
                    sent_inbox=False,
                )
            ]
        owns = owned is not None
    elif thing_type == int(ThingTypes.Character):
        owns = any(
            c.characterMasterId == thing.thing_id
            for c in await conn.fetch(get_characters(user_id))
        )

    if owns:
        converted = await grant_things_consolidated(
            conn, user_id, dupe_conversion(gacha, thing)
        )
        # every converted entry points back at what it replaced, so the client can show the
        # card that was rolled rather than a bare pile of items
        for received in converted:
            received.original_type = thing_type
            received.original_id = thing.thing_id
        if converted:
            return converted

    return [await grant_thing(conn, user_id, thing_type, thing.thing_id, quantity)]


def _gacha_selection(gacha_master_id: int):
    """``(selectable thing ids, min_select, max_select)`` for a pickup-selection gacha, or
    None if this gacha has no selection step. PickupSelectionGachaMaster covers exactly the
    72 gachas that carry ``is_selectable`` things."""
    if not _SELECTION_MASTER:
        _GACHA_MASTER.update({g.id_: g for g in cache.gacha_master})
        _SELECTION_MASTER.update(
            {p.gacha_master_id: p for p in cache.pickup_selection_gacha_master}
        )
    sel = _SELECTION_MASTER.get(gacha_master_id)
    gacha = _GACHA_MASTER.get(gacha_master_id)
    if sel is None or gacha is None:
        return None
    return (
        {t.id_ for t in gacha.things if t.is_selectable},
        sel.min_select_count,
        sel.max_select_count,
    )


# /api/Gachas/DecideReRollGacha?gachaDetailMasterId=
@router.post("/api/Gachas/DecideReRollGacha", name="Gachas_DecideReRollGacha")
async def gachas_decide_re_roll_gacha(
    request: Request, gachaDetailMasterId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Gachas
@router.get("/api/Gachas", name="Gachas_GetAvailableGachas")
async def gachas_get_available_gachas(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    # TODO: roll_left is always the full limit -- the "gacha" table stores one rollCount per
    # gacha, with no per-detail column and nothing tracking the daily reset, so spent rolls
    # cannot be attributed to a detail yet. Needs a schema change (see roll_limits()).
    out: list = []
    for gacha_master_id in active_gacha_ids():
        normal, fixed = emission_flags(gacha_master_id)
        out.append(
            GachaInfoResult(
                id=gacha_master_id,
                roll_limits=roll_limits(gacha_master_id, {}),
                normal_emission_flags=normal,
                fixed_emission_flags=fixed,
            )
        )
    return respond(out)


# /api/Gachas/CharacterLineup/{gachaMasterId}
@router.get(
    "/api/Gachas/CharacterLineup/{gachaMasterId}", name="Gachas_GetCharacterGachaLineup"
)
async def gachas_get_character_gacha_lineup(request: Request, gachaMasterId: int):
    app: YumeApp = request.app
    payload = {}  # no payload -- the gacha is the path segment
    computed = lineup(gachaMasterId)
    if computed is None:
        return respond(CharacterLineupResult())
    normal, fixed, normal_items, fixed_items = computed
    return respond(
        CharacterLineupResult(
            normal_probabilities=normal,
            fixed_probabilities=fixed,
            normal_lineup_items=normal_items,
            fixed_lineup_items=fixed_items,
        )
    )


# /api/Gachas/GetGachaHistories?cardType=
@router.post("/api/Gachas/GetGachaHistories", name="Gachas_GetGachaHistories")
async def gachas_get_gacha_histories(request: Request, cardType: Optional[int] = None):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payload = {}  # no payload -- cardType is the query string
    if user_id is None:
        return respond([])

    # one entry per prize pulled, newest first. A capture of a 10-pull returns exactly the
    # ten Poster master ids that roll awarded, all sharing that roll's timestamp.
    async with app.acquire_db() as conn:
        rows = await conn.fetch(
            get_gacha_historys(user_id, cardType or int(GachaCardTypes.Character))
        )
    return respond(
        [GachaHistoryResult(master_id=r.masterId, created_at=r.createdAt) for r in rows]
    )


# /api/Gachas/PosterLineup/{gachaMasterId}
@router.get(
    "/api/Gachas/PosterLineup/{gachaMasterId}", name="Gachas_GetPosterGachaLineup"
)
async def gachas_get_poster_gacha_lineup(request: Request, gachaMasterId: int):
    app: YumeApp = request.app
    payload = {}  # no payload -- the gacha is the path segment
    computed = lineup(gachaMasterId)
    if computed is None:
        return respond(PosterLineupResult())
    normal, fixed, normal_items, fixed_items = computed
    return respond(
        PosterLineupResult(
            normal_probabilities=normal,
            fixed_probabilities=fixed,
            normal_lineup_items=normal_items,
            fixed_lineup_items=fixed_items,
        )
    )


# /api/Gachas/GetReRollGachaResults?gachaDetailMasterId=
@router.post("/api/Gachas/GetReRollGachaResults", name="Gachas_GetReRollGachaResults")
async def gachas_get_re_roll_gacha_results(
    request: Request, gachaDetailMasterId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(GachaRollResult())


# /api/Gachas/{gachaMasterId}/SelectedThings
@router.get(
    "/api/Gachas/{gachaMasterId}/SelectedThings", name="Gachas_GetSelectedThings"
)
async def gachas_get_selected_things(request: Request, gachaMasterId: int):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payload = {}  # no payload -- the gacha is the path segment
    if user_id is None:
        return respond(GachaSelectedThingsResult())

    async with app.acquire_db() as conn:
        row = next(
            (
                r
                for r in await conn.fetch(get_gacha_selected_things(user_id))
                if r.gachaMasterId == gachaMasterId
            ),
            None,
        )
    chosen = list(row.gachaThingIds or []) if row is not None else []
    return respond(GachaSelectedThingsResult(selected_gacha_thing_ids=chosen))


# /api/Gachas/ReRollGacha?gachaDetailMasterId=
@router.post("/api/Gachas/ReRollGacha", name="Gachas_ReRollGacha")
async def gachas_re_roll_gacha(
    request: Request, gachaDetailMasterId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(GachaRollResult())


# /api/Gachas/Roll/{gachaDetailMasterId}
@router.post("/api/Gachas/Roll/{gachaDetailMasterId}", name="Gachas_RollGacha")
async def gachas_roll_gacha(request: Request, gachaDetailMasterId: int):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payload = {}  # no payload -- the detail is the path segment
    gacha, detail = detail_of(gachaDetailMasterId)
    if user_id is None or gacha is None:
        return respond(GachaRollResult())

    now = int(time.time() * 1_000_000)
    async with app.acquire_db() as conn:
        spent = await _spend_cost(conn, user_id, detail)
        if spent is None:
            return respond(GachaRollResult(), faults=[fault("NotEnoughThing")])

        prizes = roll_prizes(gacha, detail)
        card_type = int(gacha.card_type)

        # NOTE: dupes are not converted -- every prize grants the character/poster itself.
        # The real server hands back a TalentBloom item instead when you already own it
        # (captures: Rare2 character -> item 140000 x1, Rare3 -> x10; R poster -> 130063 x5,
        # SR -> 130064 x5) but the per-rarity table is server config we don't have in full,
        # so granting the possession is the deliberate stand-in. TODO once rates are known.
        results: list[GachaThingResult] = []
        for thing in prizes:
            received = await _award_prize(conn, user_id, gacha, thing)
            # a Rare4 character prize also pays out a pile of its own ActorPiece
            extra = await grant_things_consolidated(
                conn, user_id, piece_bonus(gacha, thing)
            )
            results.append(
                GachaThingResult(
                    received_things=received,
                    additional_received_things=extra,
                )
            )

        bonus = await grant_things_consolidated(
            conn,
            user_id,
            [
                (int(b.thing_type), b.thing_id, (b.thing_quantity or 0) * len(prizes))
                for b in gacha.bonus_things
            ],
        )
        detail_bonus = await grant_things_consolidated(
            conn,
            user_id,
            [
                (int(b.thing_type), b.thing_id, b.thing_quantity or 0)
                for b in detail.detail_bonus_things
            ],
        )

        await conn.execute(
            add_gacha_rolls(user_id, gacha.id_, len(prizes), _random_gacha_id())
        )
        if prizes:
            await conn.execute(
                add_gacha_historys(
                    user_id, card_type, [t.thing_id for t in prizes], now
                )
            )

    # what the roll paid out, plus what it charged -- the spent balance is a change in its
    # own right and has to show up even when nothing granted happens to share its type.
    # Read the types off the awarded things, not the prize things: a converted dupe writes
    # items, not the character/poster it was rolled from.
    refresh: set = set(spent)
    refresh |= {present_type(int(r.type)) for r in bonus + detail_bonus}
    refresh |= {
        present_type(int(r.type))
        for res in results
        for r in (res.received_things or []) + (res.additional_received_things or [])
    }
    refresh.discard(None)
    present = await build_present(app, user_id, *sorted(refresh)) if refresh else []

    return respond(
        GachaRollResult(
            # echoes the DETAIL id back, not the gacha's -- confirmed by two captures
            m_gacha_master_id=gachaDetailMasterId,
            received_things=results,
            received_bonus_things=bonus,
            received_detail_bonus_things=detail_bonus,
            # TODO: roll_bonuses (milestone rewards at N total rolls) not implemented; every
            # captured banner so far has an empty roll_bonuses list in master
            received_roll_bonus_things=[],
        ),
        present=present,
    )


# /api/Gachas/{gachaMasterId}/SetSelectedThings
@router.post(
    "/api/Gachas/{gachaMasterId}/SetSelectedThings", name="Gachas_SetSelectedThings"
)
async def gachas_set_selected_things(request: Request, gachaMasterId: int):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payload = await read_request(request, SetSelectedThingsPayload)
    if user_id is None or payload is None:
        return respond(GachaSelectedThingsResult())

    selection = _gacha_selection(gachaMasterId)
    if selection is None:
        return respond(GachaSelectedThingsResult())  # gacha has no selection step
    allowed, min_select, max_select = selection
    # keep the client's order, drop duplicates and anything this gacha does not offer as
    # selectable -- the stored selection decides real pickup odds, so it is validated here
    # rather than trusted
    chosen = [i for i in dict.fromkeys(payload.gacha_thing_ids or []) if i in allowed]
    if not min_select <= len(chosen) <= max_select:
        return respond(GachaSelectedThingsResult())

    async with app.acquire_db() as conn:
        await conn.execute(set_gacha_selected_things(user_id, gachaMasterId, chosen))

    present = await build_present(app, user_id, "GachaSelectedThings")
    return respond(
        GachaSelectedThingsResult(selected_gacha_thing_ids=chosen), present=present
    )
