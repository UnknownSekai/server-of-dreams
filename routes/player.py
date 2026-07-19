from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from db.user import get_users, mark_game_hint_read, update_user_tutorial_status
from helpers.msgpack import read_request, respond
from helpers.stamina import (
    adjust_and_check_stamina,
)  # noqa: F401  (see RecoverStaminaByJewel)
from helpers.tutorial import can_advance
from helpers.user_data import build_present, current_user_id, data_object
from models import *

router = APIRouter(tags=["Player"])


# /api/Player/RecoverStaminaByJewel?times=
@router.post("/api/Player/RecoverStaminaByJewel", name="Player_RecoverStaminaByJewel")
async def player_recover_stamina_by_jewel(
    request: Request, times: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    # TODO spend `times` jewels, then recover stamina (overfill allowed, so no clamp):
    #   async with app.acquire_db() as conn:
    #       await adjust_and_check_stamina(conn, user_id, +recover_amount, player_rank)
    return respond(BooleanResult())


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
    return respond(BooleanResult())


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
    user_id = current_user_id(request)
    payload = await read_request(request, UpdateGameHintPayload)
    categories = (
        [int(c) for c in payload.categories] if payload and payload.categories else []
    )
    present: list = []
    if user_id is not None and categories:
        async with app.acquire_db() as conn:
            for category in categories:
                await conn.execute(mark_game_hint_read(user_id, category))
        # echo the updated GameHint rows (id == pageCategory) so the client's IGameHint
        # list marks them read -- an empty marker leaves IsGameHintRead false and loops
        present = await build_present(app, user_id, ("GameHint", set(categories)))
    return respond(BooleanResult(is_success=True), present=present)


# /api/Player/UpdateHomeDisplayPreference
@router.post(
    "/api/Player/UpdateHomeDisplayPreference", name="Player_UpdateHomeDisplayPreference"
)
async def player_update_home_display_preference(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, UpdateHomeDisplayPreferencePayload)
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
    payload = await read_request(request, UpdateTutorialPayload)
    target = payload.tutorial_status if payload else TutorialStatus.Start
    user_id = current_user_id(request)
    async with app.acquire_db() as conn:
        user = await conn.fetchrow(get_users(user_id))
        if user is None or not can_advance(user.tutorialStatus, target):
            # unknown user, or a backtrack: leave the tutorial where it is
            present = [data_object("User", user)] if user is not None else []
            return respond(BooleanResult(is_success=False), present=present)
        await conn.execute(update_user_tutorial_status(user_id, int(target)))
        user = await conn.fetchrow(get_users(user_id))
    return respond(BooleanResult(is_success=True), present=[data_object("User", user)])
