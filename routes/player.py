from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import raw_response, read_request, respond
from models import *

router = APIRouter(tags=["Player"])


# /api/Player/RecoverStaminaByJewel?times=
@router.post("/api/Player/RecoverStaminaByJewel", name="Player_RecoverStaminaByJewel")
async def player_recover_stamina_by_jewel(
    request: Request, times: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(BooleanResult())


# /api/Player/ReleasePlayerRankCap
@router.post("/api/Player/ReleasePlayerRankCap", name="Player_ReleasePlayerRankCap")
async def player_release_player_rank_cap(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Player/SetHomeBGM?mHomeBGMId=&selectionType=&mHomeBGMDetailId=
@router.post("/api/Player/SetHomeBGM", name="Player_SetHomeBGM")
async def player_set_home_bgm(
    request: Request,
    mHomeBGMId: Optional[int] = None,
    selectionType: Optional[int] = None,
    mHomeBGMDetailId: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(BooleanResult())


# /api/Player/UpdateCapedPlayerRankAnnounce
@router.post(
    "/api/Player/UpdateCapedPlayerRankAnnounce",
    name="Player_UpdateCapedPlayerRankAnnounce",
)
async def player_update_caped_player_rank_announce(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Player/UpdateGameHintRead
@router.post("/api/Player/UpdateGameHintRead", name="Player_UpdateGameHintRead")
async def player_update_game_hint_read(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "UpdateGameHintPayload")
    return respond(BooleanResult())


# /api/Player/UpdateHomeDisplayPreference
@router.post(
    "/api/Player/UpdateHomeDisplayPreference", name="Player_UpdateHomeDisplayPreference"
)
async def player_update_home_display_preference(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "UpdateHomeDisplayPreferencePayload")
    return respond(BooleanResult())


# /api/Player/UpdateSplashLastDisplayTime
@router.post(
    "/api/Player/UpdateSplashLastDisplayTime",
    name="Player_UpdateHomeLastTransitionTime",
)
async def player_update_home_last_transition_time(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Player/UpdateTutorial
@router.post("/api/Player/UpdateTutorial", name="Player_UpdateTutorial")
async def player_update_tutorial(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "UpdateTutorialPayload")
    return respond(BooleanResult())
