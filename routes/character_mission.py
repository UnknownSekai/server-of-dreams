from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(tags=["CharacterMission"])


# /api/CharacterMissions/checkInitializeMissions
@router.post(
    "/api/CharacterMissions/checkInitializeMissions",
    name="CharacterMission_CheckInitializeCharacterMissions",
)
async def character_mission_check_initialize_character_missions(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/CharacterMissions/{mCharacterBaseId}/receiveAllMission
@router.post(
    "/api/CharacterMissions/{mCharacterBaseId}/receiveAllMission",
    name="CharacterMission_ReceiveAllMissionRewards",
)
async def character_mission_receive_all_mission_rewards(
    request: Request, mCharacterBaseId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(StarPointResult())


# /api/CharacterMissions/BulkReceiveAllMission
@router.post(
    "/api/CharacterMissions/BulkReceiveAllMission",
    name="CharacterMission_ReceiveAllMissionRewardsAll",
)
async def character_mission_receive_all_mission_rewards_all(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request)
    return respond([CharacterBaseStarPointResult()])


# /api/CharacterMissions/{mCharacterBaseId}/receiveKeyMission
@router.post(
    "/api/CharacterMissions/{mCharacterBaseId}/receiveKeyMission",
    name="CharacterMission_ReceiveKeyMissionRewards",
)
async def character_mission_receive_key_mission_rewards(
    request: Request, mCharacterBaseId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(StarPointResult())
