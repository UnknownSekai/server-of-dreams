from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import read_request, respond
from helpers.stamina import adjust_and_check_stamina  # noqa: F401  (see Lessons_Start)
from models import *

router = APIRouter(tags=["Lessons"])


# /api/Lessons/{characterBaseMasterId}/CreateParty
@router.post(
    "/api/Lessons/{characterBaseMasterId}/CreateParty", name="Lessons_CreateParty"
)
async def lessons_create_party(request: Request, characterBaseMasterId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Lessons/Finish
@router.post("/api/Lessons/Finish", name="Lessons_Finish")
async def lessons_finish(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, FinishLessonPayload)
    return respond(BooleanResult())


# /api/Lessons/{characterBaseMasterId}/SetParty
@router.post("/api/Lessons/{characterBaseMasterId}/SetParty", name="Lessons_SetParty")
async def lessons_set_party(request: Request, characterBaseMasterId: int):
    app: YumeApp = request.app
    payload = await read_request(request, SetLessonPartyPayload)
    return respond(BooleanResult())


# /api/Lessons/{characterBaseMasterId}/SetPartyLeader/{leaderPosition}
@router.post(
    "/api/Lessons/{characterBaseMasterId}/SetPartyLeader/{leaderPosition}",
    name="Lessons_SetPartyLeader",
)
async def lessons_set_party_leader(
    request: Request, characterBaseMasterId: int, leaderPosition: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Lessons/{characterBaseMasterId}/Start/{liveMasterId}
@router.post(
    "/api/Lessons/{characterBaseMasterId}/Start/{liveMasterId}", name="Lessons_Start"
)
async def lessons_start(
    request: Request, characterBaseMasterId: str, liveMasterId: str
):
    app: YumeApp = request.app
    payload = await read_request(request, StartLessonPayload)
    # TODO consume stamina before the lesson:
    #   async with app.acquire_db() as conn:
    #       if not await adjust_and_check_stamina(conn, user_id, -cost, player_rank):
    #           return respond(BooleanResult(is_success=False))  # not enough stamina
    return respond(BooleanResult())
