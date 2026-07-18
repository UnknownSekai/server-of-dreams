from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/Debugs", tags=["Debugs"])


# /api/Debugs/AlbumSimpleArranging
@router.post(
    "/AlbumSimpleArranging",
    response_model=BooleanResult,
    name="Debug_AlbumSimpleArranging",
)
async def debug_album_simple_arranging(
    body: DebugAlbumSimpleArrangingPayload,
) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/CacheUpdatedAt
@router.get("/CacheUpdatedAt", response_model=str, name="Debug_GetCacheUpdatedAt")
async def debug_get_cache_updated_at() -> str:
    return ""


# /api/Debugs/Circle/SupportCompanyLevelLimit
@router.post(
    "/Circle/SupportCompanyLevelLimit",
    response_model=BooleanResult,
    name="Debug_SetCircleSupportPointInfo2",
)
async def debug_set_circle_support_point_info2(
    body: SupportCompanyLevelLimitPayload,
) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/Circle/SupportPoint/StaminaLastReceivedAt/
@router.post(
    "/Circle/SupportPoint/StaminaLastReceivedAt/",
    response_model=BooleanResult,
    name="Debug_SetStaminaLastReceivedAt",
)
async def debug_set_stamina_last_received_at(lastReceivedAt: str) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/CircleUsageTimeReset?setDateTime=
@router.post(
    "/CircleUsageTimeReset",
    response_model=BooleanResult,
    name="Debug_CircleUsageTimeReset",
)
async def debug_circle_usage_time_reset(setDateTime: str) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/ConvertUserId?userId=
@router.post("/ConvertUserId", response_model=DebugUserIdResult, name="Debug_GetUsetId")
async def debug_get_uset_id(userId: str, hashedUserId: str) -> DebugUserIdResult:
    return DebugUserIdResult()


# /api/Debugs/CreateAlbum
@router.post("/CreateAlbum", response_model=BooleanResult, name="Debug_CreateAlbum")
async def debug_create_album() -> BooleanResult:
    return BooleanResult()


# /api/Debugs/DeleteCircles
@router.post("/DeleteCircles", response_model=BooleanResult, name="Debug_DeleteCircles")
async def debug_delete_circles() -> BooleanResult:
    return BooleanResult()


# /api/Debugs/DeleteLeagueAllData
@router.post(
    "/DeleteLeagueAllData",
    response_model=BooleanResult,
    name="Debug_DeleteLeagueAllData",
)
async def debug_delete_league_all_data() -> BooleanResult:
    return BooleanResult()


# /api/Debugs/DeleteLeagueUsersData
@router.post(
    "/DeleteLeagueUsersData",
    response_model=BooleanResult,
    name="Debug_DeleteLeagueUsersData",
)
async def debug_delete_league_users_data(body: list[int]) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/EditLeagueBasic
@router.post(
    "/EditLeagueBasic", response_model=BooleanResult, name="Debug_EditLeagueBasic"
)
async def debug_edit_league_basic(body: DebugEditLeagueBasicPayload) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/ExecuteLeagueTotalization
@router.post(
    "/ExecuteLeagueTotalization",
    response_model=BooleanResult,
    name="Debug_ExecuteLeagueTotalization",
)
async def debug_execute_league_totalization() -> BooleanResult:
    return BooleanResult()


# /api/Debugs/GetCurrentLeague
@router.get("/GetCurrentLeague", response_model=int, name="Debug_GetCurrentLeague")
async def debug_get_current_league() -> int:
    return 0


# /api/Debugs/GetLeagueHistories
@router.get("/GetLeagueHistories", response_model=str, name="Debug_GetLeagueHistories")
async def debug_get_league_histories() -> str:
    return ""


# /api/Debugs/GiveEnhanceItems
@router.post(
    "/GiveEnhanceItems", response_model=BooleanResult, name="Debug_GiveEnhanceItems"
)
async def debug_give_enhance_items() -> BooleanResult:
    return BooleanResult()


# /api/Debugs/GiveEnhanceItemsAndGrowCharactersMax
@router.post(
    "/GiveEnhanceItemsAndGrowCharactersMax",
    response_model=BooleanResult,
    name="Debug_GiveEnhanceItemsAndGrowCharactersMax",
)
async def debug_give_enhance_items_and_grow_characters_max() -> BooleanResult:
    return BooleanResult()


# /api/Debugs/GiveEnhanceItemsAndGrowPostersMax
@router.post(
    "/GiveEnhanceItemsAndGrowPostersMax",
    response_model=BooleanResult,
    name="Debug_GiveEnhanceItemsAndGrowPostersMax",
)
async def debug_give_enhance_items_and_grow_posters_max() -> BooleanResult:
    return BooleanResult()


# /api/Debugs/GrowAccessoriesMax
@router.post(
    "/GrowAccessoriesMax",
    response_model=BooleanResult,
    name="Debug_GiveEnhanceItemsAndGrowAccessoriesMax",
)
async def debug_give_enhance_items_and_grow_accessories_max() -> BooleanResult:
    return BooleanResult()


# /api/Debugs/InitializeLeagueBasicData
@router.post(
    "/InitializeLeagueBasicData",
    response_model=BooleanResult,
    name="Debug_InitializeLeagueBasicData",
)
async def debug_initialize_league_basic_data() -> BooleanResult:
    return BooleanResult()


# /api/Debugs/InitializePlayerRate
@router.post(
    "/InitializePlayerRate",
    response_model=BooleanResult,
    name="Debug_InitializePlayerRate",
)
async def debug_initialize_player_rate() -> BooleanResult:
    return BooleanResult()


# /api/Debugs/LiveScoreHistory
@router.get(
    "/LiveScoreHistory",
    response_model=list[ScoreWithDateResult],
    name="Debug_GetLiveScoreHistory",
)
async def debug_get_live_score_history() -> list[ScoreWithDateResult]:
    return []


# /api/Debugs/PrepareLeagueGroupUser
@router.post(
    "/PrepareLeagueGroupUser",
    response_model=BooleanResult,
    name="Debug_PrepareLeagueGroupUser",
)
async def debug_prepare_league_group_user(
    body: DebugPrepareLeagueGroupUserPayload,
) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/RefreshMemoryCache
@router.get(
    "/RefreshMemoryCache", response_model=BooleanResult, name="Debug_RefreshMemoryCache"
)
async def debug_refresh_memory_cache() -> BooleanResult:
    return BooleanResult()


# /api/Debugs/ReleaseAllMusicDifficulty
@router.post(
    "/ReleaseAllMusicDifficulty",
    response_model=BooleanResult,
    name="Debug_ReleaseAllMusicDifficulty",
)
async def debug_release_all_music_difficulty() -> BooleanResult:
    return BooleanResult()


# /api/Debugs/ResetAutoPlay
@router.post("/ResetAutoPlay", response_model=BooleanResult, name="Debug_ResetAutoPlay")
async def debug_reset_auto_play() -> BooleanResult:
    return BooleanResult()


# /api/Debugs/ResetLesson
@router.post("/ResetLesson", response_model=BooleanResult, name="Debug_ResetLesson")
async def debug_reset_lesson() -> BooleanResult:
    return BooleanResult()


# /api/Debugs/SendAccessories
@router.post(
    "/SendAccessories", response_model=BooleanResult, name="Debug_SendAccessories"
)
async def debug_send_accessories(body: list[int]) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/SendAlbumThemes
@router.post(
    "/SendAlbumThemes", response_model=BooleanResult, name="Debug_SendAlbuThemes"
)
async def debug_send_albu_themes(body: list[int]) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/SendBombs
@router.post("/SendBombs", response_model=BooleanResult, name="Debug_SendBombs")
async def debug_send_bombs(body: list[int]) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/SendCharacters
@router.post(
    "/SendCharacters", response_model=BooleanResult, name="Debug_SendCharacters"
)
async def debug_send_characters(body: AcquirableThingsPayload) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/SendChatworkMessage
@router.post(
    "/SendChatworkMessage",
    response_model=BooleanResult,
    name="Debug_SendChatworkMessage",
)
async def debug_send_chatwork_message(
    body: ChatworkSendMessagePayload,
) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/SendCostumes
@router.post("/SendCostumes", response_model=BooleanResult, name="Debug_SendCostumes")
async def debug_send_costumes(body: list[int]) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/SendDecorations
@router.post(
    "/SendDecorations", response_model=BooleanResult, name="Debug_SendDecorations"
)
async def debug_send_decorations(body: list[int]) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/SendHomeSkins
@router.post("/SendHomeSkins", response_model=BooleanResult, name="Debug_SendHomeSkins")
async def debug_send_home_skins(body: list[int]) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/SendIconFrames
@router.post(
    "/SendIconFrames", response_model=BooleanResult, name="Debug_SendIconFrames"
)
async def debug_send_icon_frames(body: list[int]) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/SendItems
@router.post("/SendItems", response_model=BooleanResult, name="Debug_SendItems")
async def debug_send_items(body: AcquirableThingsPayload) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/SendMusics
@router.post("/SendMusics", response_model=BooleanResult, name="Debug_SendMusics")
async def debug_send_musics(body: list[int]) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/SendNameBaseColors
@router.post(
    "/SendNameBaseColors", response_model=BooleanResult, name="Debug_SendNameBaseColors"
)
async def debug_send_name_base_colors(body: list[int]) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/SendNameColors
@router.post(
    "/SendNameColors", response_model=BooleanResult, name="Debug_SendNameColors"
)
async def debug_send_name_colors(body: list[int]) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/SendNameplates
@router.post(
    "/SendNameplates", response_model=BooleanResult, name="Debug_SendNameplates"
)
async def debug_send_nameplates(body: list[int]) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/SendNotes
@router.post("/SendNotes", response_model=BooleanResult, name="Debug_SendNotes")
async def debug_send_notes(body: list[int]) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/SendNotification
@router.post(
    "/SendNotification", response_model=BooleanResult, name="Debug_SendNotification"
)
async def debug_send_notification() -> BooleanResult:
    return BooleanResult()


# /api/Debugs/SendPosters
@router.post("/SendPosters", response_model=BooleanResult, name="Debug_SendPosters")
async def debug_send_posters(body: AcquirableThingsPayload) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/SendStamps
@router.post("/SendStamps", response_model=BooleanResult, name="Debug_SendStamp")
async def debug_send_stamp(body: list[int]) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/SendTrophies
@router.post("/SendTrophies", response_model=BooleanResult, name="Debug_SendTrophies")
async def debug_send_trophies(body: list[int]) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/SetCharacterEnhanceInfo
@router.post(
    "/SetCharacterEnhanceInfo",
    response_model=BooleanResult,
    name="Debug_SetCharacterEnhanceInfo",
)
async def debug_set_character_enhance_info(
    body: list[DebugModifyCharacterEnhanceInformationPayload],
) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/SetLoginPassUntil?until=
@router.post(
    "/SetLoginPassUntil", response_model=BooleanResult, name="Debug_SetLoginPassUntil"
)
async def debug_set_login_pass_until(until: str) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/SetPlayerRate?rate=
@router.post("/SetPlayerRate", response_model=BooleanResult, name="Debug_SetPlayerRate")
async def debug_set_player_rate(rate: str) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/SetPosterEnhanceInfo
@router.post(
    "/SetPosterEnhanceInfo",
    response_model=BooleanResult,
    name="Debug_SetPosterEnhanceInfo",
)
async def debug_set_poster_enhance_info(
    body: list[DebugModifyPosterEnhanceInformationPayload],
) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/SetServerTime?dateTime=
@router.post("/SetServerTime", response_model=BooleanResult, name="Debug_SetServerTime")
async def debug_set_server_time(dateTime: str) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/SetSplashLastDisplayedAt?displayedAtText=
@router.post(
    "/SetSplashLastDisplayedAt",
    response_model=BooleanResult,
    name="Debug_SetSplashLastDisplayedAt",
)
async def debug_set_splash_last_displayed_at(displayedAtText: str) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/SetTimeWarpByDate?setDateTime=
@router.post(
    "/SetTimeWarpByDate", response_model=BooleanResult, name="Debug_SetTimeWarpByDate"
)
async def debug_set_time_warp_by_date(setDateTime: str) -> BooleanResult:
    return BooleanResult()


# /api/Debugs/UnlockAllFeatures
@router.post(
    "/UnlockAllFeatures", response_model=BooleanResult, name="Debug_UnlockAllFeatures"
)
async def debug_unlock_all_features() -> BooleanResult:
    return BooleanResult()


# /api/Debugs/UploadToutchLog
@router.post("/UploadToutchLog", response_model=UrlResult, name="Debug_UploadToutchLog")
async def debug_upload_toutch_log(body: str) -> UrlResult:
    return UrlResult()


# /api/Debugs/Yokubari
@router.post("/Yokubari", response_model=BooleanResult, name="Debug_GrantAllThing")
async def debug_grant_all_thing() -> BooleanResult:
    return BooleanResult()
