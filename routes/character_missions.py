from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/CharacterMissions", tags=["CharacterMissions"])


# /api/CharacterMissions/BulkReceiveAllMission
@router.post(
    "/BulkReceiveAllMission", name="CharacterMission_ReceiveAllMissionRewardsAll"
)
async def character_mission_receive_all_mission_rewards_all(request: Request):
    payload = await read_request(request, None)
    return respond([])


# /api/CharacterMissions/checkInitializeMissions
@router.post(
    "/checkInitializeMissions", name="CharacterMission_CheckInitializeCharacterMissions"
)
async def character_mission_check_initialize_character_missions(request: Request):
    return respond(BooleanResult())
