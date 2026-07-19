from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(tags=["Party"])


# /api/Parties/{uPartyId}/ChangeName
@router.post("/api/Parties/{uPartyId}/ChangeName", name="Party_ChangePartyName")
async def party_change_party_name(request: Request, uPartyId: int):
    app: YumeApp = request.app
    payload = await read_request(request, ChangeNamePayload)
    return respond(BooleanResult())


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
    payload = await read_request(request, EditPartyPayload)
    return respond(BooleanResult())


# /api/Parties/{uPartyId}/SetLeader/{leaderPosition}
@router.post(
    "/api/Parties/{uPartyId}/SetLeader/{leaderPosition}", name="Party_EditParty2"
)
async def party_edit_party2(request: Request, uPartyId: int, leaderPosition: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Parties/{uPartyId}/EditPosition
@router.post("/api/Parties/{uPartyId}/EditPosition", name="Party_EditPartyPosition")
async def party_edit_party_position(request: Request, uPartyId: int):
    app: YumeApp = request.app
    payload = await read_request(request, EditPositionPayload)
    return respond(BooleanResult())


# /api/Parties/{uPartyId}/EditPartyWithRecommended
@router.post(
    "/api/Parties/{uPartyId}/EditPartyWithRecommended",
    name="Party_EditPartyWithRecommended",
)
async def party_edit_party_with_recommended(request: Request, uPartyId: int):
    app: YumeApp = request.app
    payload = await read_request(request, EditPartyPayload)
    return respond(BooleanResult())


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
    payload = {}  # no payload
    return respond(BooleanResult())


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
