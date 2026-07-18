from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/Player", tags=["Player"])


# /api/Player/ReleasePlayerRankCap
@router.post(
    "/ReleasePlayerRankCap",
    response_model=BooleanResult,
    name="Player_ReleasePlayerRankCap",
)
async def player_release_player_rank_cap() -> BooleanResult:
    return BooleanResult()


# /api/Player/UpdateCapedPlayerRankAnnounce
@router.post(
    "/UpdateCapedPlayerRankAnnounce",
    response_model=BooleanResult,
    name="Player_UpdateCapedPlayerRankAnnounce",
)
async def player_update_caped_player_rank_announce() -> BooleanResult:
    return BooleanResult()


# /api/Player/UpdateGameHintRead
@router.post(
    "/UpdateGameHintRead",
    response_model=BooleanResult,
    name="Player_UpdateGameHintRead",
)
async def player_update_game_hint_read(body: UpdateGameHintPayload) -> BooleanResult:
    return BooleanResult()


# /api/Player/UpdateHomeDisplayPreference
@router.post(
    "/UpdateHomeDisplayPreference",
    response_model=BooleanResult,
    name="Player_UpdateHomeDisplayPreference",
)
async def player_update_home_display_preference(
    body: UpdateHomeDisplayPreferencePayload,
) -> BooleanResult:
    return BooleanResult()


# /api/Player/UpdateSplashLastDisplayTime
@router.post(
    "/UpdateSplashLastDisplayTime",
    response_model=BooleanResult,
    name="Player_UpdateHomeLastTransitionTime",
)
async def player_update_home_last_transition_time() -> BooleanResult:
    return BooleanResult()


# /api/Player/UpdateTutorial
@router.post(
    "/UpdateTutorial", response_model=BooleanResult, name="Player_UpdateTutorial"
)
async def player_update_tutorial(body: UpdateTutorialPayload) -> BooleanResult:
    return BooleanResult()
