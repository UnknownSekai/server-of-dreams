from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from db.user import (
    get_party_slots,
    get_partys,
    get_user_preferences,
    update_multi_party,
    update_party_leader,
    update_party_name,
    update_party_slot_positions,
    update_party_slots,
)
from helpers.msgpack import read_request, respond
from helpers.user_data import current_user_id, data_object
from models import *
from models.database import PartySlotModel

router = APIRouter(tags=["Party"])


async def _apply_slot_edits(conn, user_id: int, payload: EditPartyPayload) -> list:
    """Write an EditParty-shaped loadout onto the caller's slots. The client submits the
    party's full slot list every time, so diff against what is stored -- only the slots that
    actually moved are written, and only those go in present."""
    owned = {s.id: s for s in await conn.fetch(get_party_slots(user_id))}
    changed: list[PartySlotModel] = []
    for edit in payload.party_slots or []:
        slot = owned.get(edit.u_party_slot_id)
        if slot is None:
            continue  # not one of this user's slots -- ignore, never create
        updated = slot.model_copy(
            update={
                "characterId": edit.u_character_id,
                # NB the payload orders these accessory-then-poster, the reverse of the
                # PartySlot entity -- confirmed against a capture, don't "fix" it
                "posterId": edit.u_poster_id,
                "accessoryId": edit.u_accessory_id,
                "bonusAbilityEnableFlags": int(edit.bonus_ability_enable_flags),
            }
        )
        if updated != slot:
            changed.append(updated)
    if not changed:
        return []
    await conn.execute(update_party_slots(user_id, changed))
    return [data_object("PartySlot", s) for s in changed]


async def _set_leader(conn, user_id: int, party_id: int, position: int) -> list:
    """Move a party's leader marker; returns the present entries for what changed."""
    party = next(
        (p for p in await conn.fetch(get_partys(user_id)) if p.id == party_id), None
    )
    if party is None or party.leaderPosition == position:
        return []
    await conn.execute(update_party_leader(user_id, party_id, position))
    party.leaderPosition = position
    return [data_object("Party", party)]


# /api/Parties/{uPartyId}/ChangeName
@router.post("/api/Parties/{uPartyId}/ChangeName", name="Party_ChangePartyName")
async def party_change_party_name(request: Request, uPartyId: int):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payload = await read_request(request, ChangeNamePayload)
    if user_id is None or payload is None or payload.name is None:
        return respond(BooleanResult())

    present: list = []
    async with app.acquire_db() as conn:
        party = next(
            (p for p in await conn.fetch(get_partys(user_id)) if p.id == uPartyId), None
        )
        if party is None:
            return respond(BooleanResult())  # not the caller's party
        if party.name != payload.name:
            await conn.execute(update_party_name(user_id, uPartyId, payload.name))
            party.name = payload.name
            present = [data_object("Party", party)]
    return respond(BooleanResult(is_success=True), present=present)


# /api/Parties/ChangeTripleCastPartyName?partyOrder=&newName=
@router.post(
    "/api/Parties/ChangeTripleCastPartyName", name="Party_ChangeTripleCastPartyName"
)
async def party_change_triple_cast_party_name(
    request: Request, partyOrder: Optional[int] = None, newName: Optional[str] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Parties/{srcOrder}/CopyTo/{destOrder}
@router.post("/api/Parties/{srcOrder}/CopyTo/{destOrder}", name="Party_CopyParty")
async def party_copy_party(request: Request, srcOrder: int, destOrder: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Parties/{uPartyId}/EditParty
@router.post("/api/Parties/{uPartyId}/EditParty", name="Party_EditParty")
async def party_edit_party(request: Request, uPartyId: int):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payload = await read_request(request, EditPartyPayload)
    if user_id is None or payload is None:
        return respond(BooleanResult())

    async with app.acquire_db() as conn:
        present = await _apply_slot_edits(conn, user_id, payload)
        # leader_position rides along on the same payload (null = leave it alone) and lives
        # on the party row, not the slots
        if payload.leader_position is not None:
            present += await _set_leader(
                conn, user_id, uPartyId, payload.leader_position
            )
    return respond(BooleanResult(is_success=True), present=present)


# /api/Parties/{uPartyId}/SetLeader/{leaderPosition}
@router.post(
    "/api/Parties/{uPartyId}/SetLeader/{leaderPosition}", name="Party_EditParty2"
)
async def party_edit_party2(request: Request, uPartyId: int, leaderPosition: int):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payload = {}  # no payload -- both operands are path segments
    if user_id is None:
        return respond(BooleanResult())

    async with app.acquire_db() as conn:
        present = await _set_leader(conn, user_id, uPartyId, leaderPosition)
    return respond(BooleanResult(is_success=True), present=present)


# /api/Parties/{uPartyId}/EditPosition
@router.post("/api/Parties/{uPartyId}/EditPosition", name="Party_EditPartyPosition")
async def party_edit_party_position(request: Request, uPartyId: int):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payload = await read_request(request, EditPositionPayload)
    if user_id is None or payload is None:
        return respond(BooleanResult())

    present: list = []
    async with app.acquire_db() as conn:
        owned = {s.id: s for s in await conn.fetch(get_party_slots(user_id))}
        changed: list[PartySlotModel] = []
        for edit in payload.slots or []:
            slot = owned.get(edit.u_party_slot_id)
            if slot is None or slot.position == edit.position:
                continue
            changed.append(slot.model_copy(update={"position": edit.position}))
        if changed:
            # a reorder is a permutation, so the whole set moves at once -- one statement,
            # no intermediate state where two slots share a position
            await conn.execute(
                update_party_slot_positions(
                    user_id, [(s.id, s.position) for s in changed]
                )
            )
            present = [data_object("PartySlot", s) for s in changed]
    return respond(BooleanResult(is_success=True), present=present)


# /api/Parties/{uPartyId}/EditPartyWithRecommended
@router.post(
    "/api/Parties/{uPartyId}/EditPartyWithRecommended",
    name="Party_EditPartyWithRecommended",
)
async def party_edit_party_with_recommended(request: Request, uPartyId: int):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payload = await read_request(request, EditPartyPayload)
    if user_id is None or payload is None:
        return respond(BooleanResult())

    # the client picks the recommended members itself and submits them in the same shape as
    # a manual edit, so this is the same write -- the "recommend" part is entirely client-side
    async with app.acquire_db() as conn:
        present = await _apply_slot_edits(conn, user_id, payload)
        if payload.leader_position is not None:
            present += await _set_leader(
                conn, user_id, uPartyId, payload.leader_position
            )
    return respond(BooleanResult(is_success=True), present=present)


# /api/Parties/EditTripleCastBasic?partyOrder=&tripleCastGroupOrder=
@router.post("/api/Parties/EditTripleCastBasic", name="Party_EditTripleCastBasic")
async def party_edit_triple_cast_basic(
    request: Request,
    partyOrder: Optional[int] = None,
    tripleCastGroupOrder: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Parties/EditTripleCastParty?partyOrder=
@router.post("/api/Parties/EditTripleCastParty", name="Party_EditTripleCastParty")
async def party_edit_triple_cast_party(
    request: Request, partyOrder: Optional[int] = None
):
    app: YumeApp = request.app
    payload = await read_request(request, EditPartyPayload)
    return respond(BooleanResult())


# /api/Parties/EditTripleCastPartySlotPosition?partyOrder=
@router.post(
    "/api/Parties/EditTripleCastPartySlotPosition",
    name="Party_EditTripleCastPartySlotPosition",
)
async def party_edit_triple_cast_party_slot_position(
    request: Request, partyOrder: Optional[int] = None
):
    app: YumeApp = request.app
    payload = await read_request(request, EditPositionPayload)
    return respond(BooleanResult())


# /api/Parties/{uPartyId}/SetMultiParty
@router.post("/api/Parties/{uPartyId}/SetMultiParty", name="Party_SetMultiParty")
async def party_set_multi_party(request: Request, uPartyId: int):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payload = {}  # no payload -- the party is the path segment
    if user_id is None:
        return respond(BooleanResult())

    # "which of my parties do I bring to multi-live" is a user preference, not party state
    present: list = []
    async with app.acquire_db() as conn:
        pref = next(iter(await conn.fetch(get_user_preferences(user_id))), None)
        if pref is not None and pref.multiPartyId != uPartyId:
            await conn.execute(update_multi_party(user_id, uPartyId))
            pref.multiPartyId = uPartyId
            present = [data_object("UserPreference", pref)]
    return respond(BooleanResult(is_success=True), present=present)


# /api/Parties/SetTripleCastPartyLeaderPosition?partyOrder=&leaderPosition=
@router.post(
    "/api/Parties/SetTripleCastPartyLeaderPosition",
    name="Party_SetTripleCastPartyLeaderPosition",
)
async def party_set_triple_cast_party_leader_position(
    request: Request,
    partyOrder: Optional[int] = None,
    leaderPosition: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())
