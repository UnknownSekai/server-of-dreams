from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/CharacterMissions", tags=["CharacterMissions"])


# /api/CharacterMissions/BulkReceiveAllMission
@router.post(
    "/BulkReceiveAllMission",
    response_model=list[CharacterBaseStarPointResult],
    name="CharacterMission_ReceiveAllMissionRewardsAll",
)
async def character_mission_receive_all_mission_rewards_all(
    body: list[int],
) -> list[CharacterBaseStarPointResult]:
    return []


# /api/CharacterMissions/checkInitializeMissions
@router.post(
    "/checkInitializeMissions",
    response_model=BooleanResult,
    name="CharacterMission_CheckInitializeCharacterMissions",
)
async def character_mission_check_initialize_character_missions() -> BooleanResult:
    return BooleanResult()
