from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(tags=["Mission"])


# /api/Missions/PickupActor/bulkReceiveRewards/{mPickupCharacterMissionMasterId}
@router.post(
    "/api/Missions/PickupActor/bulkReceiveRewards/{mPickupCharacterMissionMasterId}",
    name="Mission_BulkReceivePiclupCharacterMissionRewards",
)
async def mission_bulk_receive_piclup_character_mission_rewards(
    request: Request, mPickupCharacterMissionMasterId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])


# /api/Missions/ExchangeMissionPoint?unit=
@router.post("/api/Missions/ExchangeMissionPoint", name="Mission_ExchangeMissionPoint")
async def mission_exchange_mission_point(request: Request, unit: Optional[int] = None):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Missions/receiveRewards?missionCategory=
@router.post("/api/Missions/receiveRewards", name="Mission_ReceiveAllCurrentReward")
async def mission_receive_all_current_reward(
    request: Request, missionCategory: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])


# /api/Missions/MissionPassReceiveRewards/{missionPassId}
@router.post(
    "/api/Missions/MissionPassReceiveRewards/{missionPassId}",
    name="Mission_ReceiveBulkMissionPassRewards",
)
async def mission_receive_bulk_mission_pass_rewards(
    request: Request, missionPassId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(MissionPassRewardsResult())


# /api/Missions/{missionId}/receiveCurrentRewards
@router.post(
    "/api/Missions/{missionId}/receiveCurrentRewards",
    name="Mission_ReceiveCurrentReward",
)
async def mission_receive_current_reward(request: Request, missionId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])


# /api/Missions/PickupActor/receiveRewards/{mPickupCharacterMissionMasterId}/{mPickupCharacterMissionDetailMasterId}
@router.post(
    "/api/Missions/PickupActor/receiveRewards/{mPickupCharacterMissionMasterId}/{mPickupCharacterMissionDetailMasterId}",
    name="Mission_ReceivePiclupCharacterMissionRewards",
)
async def mission_receive_piclup_character_mission_rewards(
    request: Request,
    mPickupCharacterMissionMasterId: int,
    mPickupCharacterMissionDetailMasterId: int,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])
