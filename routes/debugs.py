from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/Debugs", tags=["Debugs"])


# /api/Debugs/AlbumSimpleArranging
@router.post("/AlbumSimpleArranging", name="Debug_AlbumSimpleArranging")
async def debug_album_simple_arranging(request: Request):
    payload = await read_request(request, "DebugAlbumSimpleArrangingPayload")
    return respond(BooleanResult())


# /api/Debugs/CacheUpdatedAt
@router.get("/CacheUpdatedAt", name="Debug_GetCacheUpdatedAt")
async def debug_get_cache_updated_at(request: Request):
    return respond("")


# /api/Debugs/Circle/SupportCompanyLevelLimit
@router.post(
    "/Circle/SupportCompanyLevelLimit", name="Debug_SetCircleSupportPointInfo2"
)
async def debug_set_circle_support_point_info2(request: Request):
    payload = await read_request(request, "SupportCompanyLevelLimitPayload")
    return respond(BooleanResult())


# /api/Debugs/Circle/SupportPoint/StaminaLastReceivedAt/
@router.post(
    "/Circle/SupportPoint/StaminaLastReceivedAt/", name="Debug_SetStaminaLastReceivedAt"
)
async def debug_set_stamina_last_received_at(request: Request):
    return respond(BooleanResult())


# /api/Debugs/CircleUsageTimeReset?setDateTime=
@router.post("/CircleUsageTimeReset", name="Debug_CircleUsageTimeReset")
async def debug_circle_usage_time_reset(request: Request):
    return respond(BooleanResult())


# /api/Debugs/ConvertUserId?userId=
@router.post("/ConvertUserId", name="Debug_GetUsetId")
async def debug_get_uset_id(request: Request):
    return respond(DebugUserIdResult())


# /api/Debugs/CreateAlbum
@router.post("/CreateAlbum", name="Debug_CreateAlbum")
async def debug_create_album(request: Request):
    return respond(BooleanResult())


# /api/Debugs/DeleteCircles
@router.post("/DeleteCircles", name="Debug_DeleteCircles")
async def debug_delete_circles(request: Request):
    return respond(BooleanResult())


# /api/Debugs/DeleteLeagueAllData
@router.post("/DeleteLeagueAllData", name="Debug_DeleteLeagueAllData")
async def debug_delete_league_all_data(request: Request):
    return respond(BooleanResult())


# /api/Debugs/DeleteLeagueUsersData
@router.post("/DeleteLeagueUsersData", name="Debug_DeleteLeagueUsersData")
async def debug_delete_league_users_data(request: Request):
    payload = await read_request(request, None)
    return respond(BooleanResult())


# /api/Debugs/EditLeagueBasic
@router.post("/EditLeagueBasic", name="Debug_EditLeagueBasic")
async def debug_edit_league_basic(request: Request):
    payload = await read_request(request, "DebugEditLeagueBasicPayload")
    return respond(BooleanResult())


# /api/Debugs/ExecuteLeagueTotalization
@router.post("/ExecuteLeagueTotalization", name="Debug_ExecuteLeagueTotalization")
async def debug_execute_league_totalization(request: Request):
    return respond(BooleanResult())


# /api/Debugs/GetCurrentLeague
@router.get("/GetCurrentLeague", name="Debug_GetCurrentLeague")
async def debug_get_current_league(request: Request):
    return respond(0)


# /api/Debugs/GetLeagueHistories
@router.get("/GetLeagueHistories", name="Debug_GetLeagueHistories")
async def debug_get_league_histories(request: Request):
    return respond("")


# /api/Debugs/GiveEnhanceItems
@router.post("/GiveEnhanceItems", name="Debug_GiveEnhanceItems")
async def debug_give_enhance_items(request: Request):
    return respond(BooleanResult())


# /api/Debugs/GiveEnhanceItemsAndGrowCharactersMax
@router.post(
    "/GiveEnhanceItemsAndGrowCharactersMax",
    name="Debug_GiveEnhanceItemsAndGrowCharactersMax",
)
async def debug_give_enhance_items_and_grow_characters_max(request: Request):
    return respond(BooleanResult())


# /api/Debugs/GiveEnhanceItemsAndGrowPostersMax
@router.post(
    "/GiveEnhanceItemsAndGrowPostersMax", name="Debug_GiveEnhanceItemsAndGrowPostersMax"
)
async def debug_give_enhance_items_and_grow_posters_max(request: Request):
    return respond(BooleanResult())


# /api/Debugs/GrowAccessoriesMax
@router.post("/GrowAccessoriesMax", name="Debug_GiveEnhanceItemsAndGrowAccessoriesMax")
async def debug_give_enhance_items_and_grow_accessories_max(request: Request):
    return respond(BooleanResult())


# /api/Debugs/InitializeLeagueBasicData
@router.post("/InitializeLeagueBasicData", name="Debug_InitializeLeagueBasicData")
async def debug_initialize_league_basic_data(request: Request):
    return respond(BooleanResult())


# /api/Debugs/InitializePlayerRate
@router.post("/InitializePlayerRate", name="Debug_InitializePlayerRate")
async def debug_initialize_player_rate(request: Request):
    return respond(BooleanResult())


# /api/Debugs/LiveScoreHistory
@router.get("/LiveScoreHistory", name="Debug_GetLiveScoreHistory")
async def debug_get_live_score_history(request: Request):
    return respond([])


# /api/Debugs/PrepareLeagueGroupUser
@router.post("/PrepareLeagueGroupUser", name="Debug_PrepareLeagueGroupUser")
async def debug_prepare_league_group_user(request: Request):
    payload = await read_request(request, "DebugPrepareLeagueGroupUserPayload")
    return respond(BooleanResult())


# /api/Debugs/RefreshMemoryCache
@router.get("/RefreshMemoryCache", name="Debug_RefreshMemoryCache")
async def debug_refresh_memory_cache(request: Request):
    return respond(BooleanResult())


# /api/Debugs/ReleaseAllMusicDifficulty
@router.post("/ReleaseAllMusicDifficulty", name="Debug_ReleaseAllMusicDifficulty")
async def debug_release_all_music_difficulty(request: Request):
    return respond(BooleanResult())


# /api/Debugs/ResetAutoPlay
@router.post("/ResetAutoPlay", name="Debug_ResetAutoPlay")
async def debug_reset_auto_play(request: Request):
    return respond(BooleanResult())


# /api/Debugs/ResetLesson
@router.post("/ResetLesson", name="Debug_ResetLesson")
async def debug_reset_lesson(request: Request):
    return respond(BooleanResult())


# /api/Debugs/SendAccessories
@router.post("/SendAccessories", name="Debug_SendAccessories")
async def debug_send_accessories(request: Request):
    payload = await read_request(request, None)
    return respond(BooleanResult())


# /api/Debugs/SendAlbumThemes
@router.post("/SendAlbumThemes", name="Debug_SendAlbuThemes")
async def debug_send_albu_themes(request: Request):
    payload = await read_request(request, None)
    return respond(BooleanResult())


# /api/Debugs/SendBombs
@router.post("/SendBombs", name="Debug_SendBombs")
async def debug_send_bombs(request: Request):
    payload = await read_request(request, None)
    return respond(BooleanResult())


# /api/Debugs/SendCharacters
@router.post("/SendCharacters", name="Debug_SendCharacters")
async def debug_send_characters(request: Request):
    payload = await read_request(request, "AcquirableThingsPayload")
    return respond(BooleanResult())


# /api/Debugs/SendChatworkMessage
@router.post("/SendChatworkMessage", name="Debug_SendChatworkMessage")
async def debug_send_chatwork_message(request: Request):
    payload = await read_request(request, "ChatworkSendMessagePayload")
    return respond(BooleanResult())


# /api/Debugs/SendCostumes
@router.post("/SendCostumes", name="Debug_SendCostumes")
async def debug_send_costumes(request: Request):
    payload = await read_request(request, None)
    return respond(BooleanResult())


# /api/Debugs/SendDecorations
@router.post("/SendDecorations", name="Debug_SendDecorations")
async def debug_send_decorations(request: Request):
    payload = await read_request(request, None)
    return respond(BooleanResult())


# /api/Debugs/SendHomeSkins
@router.post("/SendHomeSkins", name="Debug_SendHomeSkins")
async def debug_send_home_skins(request: Request):
    payload = await read_request(request, None)
    return respond(BooleanResult())


# /api/Debugs/SendIconFrames
@router.post("/SendIconFrames", name="Debug_SendIconFrames")
async def debug_send_icon_frames(request: Request):
    payload = await read_request(request, None)
    return respond(BooleanResult())


# /api/Debugs/SendItems
@router.post("/SendItems", name="Debug_SendItems")
async def debug_send_items(request: Request):
    payload = await read_request(request, "AcquirableThingsPayload")
    return respond(BooleanResult())


# /api/Debugs/SendMusics
@router.post("/SendMusics", name="Debug_SendMusics")
async def debug_send_musics(request: Request):
    payload = await read_request(request, None)
    return respond(BooleanResult())


# /api/Debugs/SendNameBaseColors
@router.post("/SendNameBaseColors", name="Debug_SendNameBaseColors")
async def debug_send_name_base_colors(request: Request):
    payload = await read_request(request, None)
    return respond(BooleanResult())


# /api/Debugs/SendNameColors
@router.post("/SendNameColors", name="Debug_SendNameColors")
async def debug_send_name_colors(request: Request):
    payload = await read_request(request, None)
    return respond(BooleanResult())


# /api/Debugs/SendNameplates
@router.post("/SendNameplates", name="Debug_SendNameplates")
async def debug_send_nameplates(request: Request):
    payload = await read_request(request, None)
    return respond(BooleanResult())


# /api/Debugs/SendNotes
@router.post("/SendNotes", name="Debug_SendNotes")
async def debug_send_notes(request: Request):
    payload = await read_request(request, None)
    return respond(BooleanResult())


# /api/Debugs/SendNotification
@router.post("/SendNotification", name="Debug_SendNotification")
async def debug_send_notification(request: Request):
    return respond(BooleanResult())


# /api/Debugs/SendPosters
@router.post("/SendPosters", name="Debug_SendPosters")
async def debug_send_posters(request: Request):
    payload = await read_request(request, "AcquirableThingsPayload")
    return respond(BooleanResult())


# /api/Debugs/SendStamps
@router.post("/SendStamps", name="Debug_SendStamp")
async def debug_send_stamp(request: Request):
    payload = await read_request(request, None)
    return respond(BooleanResult())


# /api/Debugs/SendTrophies
@router.post("/SendTrophies", name="Debug_SendTrophies")
async def debug_send_trophies(request: Request):
    payload = await read_request(request, None)
    return respond(BooleanResult())


# /api/Debugs/SetCharacterEnhanceInfo
@router.post("/SetCharacterEnhanceInfo", name="Debug_SetCharacterEnhanceInfo")
async def debug_set_character_enhance_info(request: Request):
    payload = await read_request(request, None)
    return respond(BooleanResult())


# /api/Debugs/SetLoginPassUntil?until=
@router.post("/SetLoginPassUntil", name="Debug_SetLoginPassUntil")
async def debug_set_login_pass_until(request: Request):
    return respond(BooleanResult())


# /api/Debugs/SetPlayerRate?rate=
@router.post("/SetPlayerRate", name="Debug_SetPlayerRate")
async def debug_set_player_rate(request: Request):
    return respond(BooleanResult())


# /api/Debugs/SetPosterEnhanceInfo
@router.post("/SetPosterEnhanceInfo", name="Debug_SetPosterEnhanceInfo")
async def debug_set_poster_enhance_info(request: Request):
    payload = await read_request(request, None)
    return respond(BooleanResult())


# /api/Debugs/SetServerTime?dateTime=
@router.post("/SetServerTime", name="Debug_SetServerTime")
async def debug_set_server_time(request: Request):
    return respond(BooleanResult())


# /api/Debugs/SetSplashLastDisplayedAt?displayedAtText=
@router.post("/SetSplashLastDisplayedAt", name="Debug_SetSplashLastDisplayedAt")
async def debug_set_splash_last_displayed_at(request: Request):
    return respond(BooleanResult())


# /api/Debugs/SetTimeWarpByDate?setDateTime=
@router.post("/SetTimeWarpByDate", name="Debug_SetTimeWarpByDate")
async def debug_set_time_warp_by_date(request: Request):
    return respond(BooleanResult())


# /api/Debugs/UnlockAllFeatures
@router.post("/UnlockAllFeatures", name="Debug_UnlockAllFeatures")
async def debug_unlock_all_features(request: Request):
    return respond(BooleanResult())


# /api/Debugs/UploadToutchLog
@router.post("/UploadToutchLog", name="Debug_UploadToutchLog")
async def debug_upload_toutch_log(request: Request):
    payload = await read_request(request, None)
    return respond(UrlResult())


# /api/Debugs/Yokubari
@router.post("/Yokubari", name="Debug_GrantAllThing")
async def debug_grant_all_thing(request: Request):
    return respond(BooleanResult())
