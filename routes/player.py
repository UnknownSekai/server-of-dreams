from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/Player", tags=["Player"])


# /api/Player/ReleasePlayerRankCap
@router.post("/ReleasePlayerRankCap", name="Player_ReleasePlayerRankCap")
async def player_release_player_rank_cap(request: Request):
    return respond(BooleanResult())


# /api/Player/UpdateCapedPlayerRankAnnounce
@router.post(
    "/UpdateCapedPlayerRankAnnounce", name="Player_UpdateCapedPlayerRankAnnounce"
)
async def player_update_caped_player_rank_announce(request: Request):
    return respond(BooleanResult())


# /api/Player/UpdateGameHintRead
@router.post("/UpdateGameHintRead", name="Player_UpdateGameHintRead")
async def player_update_game_hint_read(request: Request):
    payload = await read_request(request, "UpdateGameHintPayload")
    return respond(BooleanResult())


# /api/Player/UpdateHomeDisplayPreference
@router.post("/UpdateHomeDisplayPreference", name="Player_UpdateHomeDisplayPreference")
async def player_update_home_display_preference(request: Request):
    payload = await read_request(request, "UpdateHomeDisplayPreferencePayload")
    return respond(BooleanResult())


# /api/Player/UpdateSplashLastDisplayTime
@router.post("/UpdateSplashLastDisplayTime", name="Player_UpdateHomeLastTransitionTime")
async def player_update_home_last_transition_time(request: Request):
    return respond(BooleanResult())


# /api/Player/UpdateTutorial
@router.post("/UpdateTutorial", name="Player_UpdateTutorial")
async def player_update_tutorial(request: Request):
    payload = await read_request(request, "UpdateTutorialPayload")
    return respond(BooleanResult())
