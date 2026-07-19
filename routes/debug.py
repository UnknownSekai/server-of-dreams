from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(tags=["Debug"])


# /api/Debugs/CircleEvent/AddCircleEventMissionCount?mCircleEventMissionId=&addCount=
@router.post(
    "/api/Debugs/CircleEvent/AddCircleEventMissionCount",
    name="Debug_AddCircleEventMissionCount",
)
async def debug_add_circle_event_mission_count(
    request: Request,
    mCircleEventMissionId: Optional[int] = None,
    addCount: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/AddCircleMembers/{count}
@router.post("/api/Debugs/AddCircleMembers/{count}", name="Debug_AddCircleMembers")
async def debug_add_circle_members(request: Request, count: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/AddExceededStarPoint/{mCharacterBaseId}/{amount}
@router.post(
    "/api/Debugs/AddExceededStarPoint/{mCharacterBaseId}/{amount}",
    name="Debug_AddExceededStarPoint",
)
async def debug_add_exceeded_star_point(
    request: Request, mCharacterBaseId: int, amount: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/AddLessonHighScore/{addScore}
@router.post(
    "/api/Debugs/AddLessonHighScore/{addScore}", name="Debug_AddLessonHighScore"
)
async def debug_add_lesson_high_score(request: Request, addScore: int):
    app: YumeApp = request.app
    payload = await read_request(request)
    return respond(BooleanResult())


# /api/Debugs/AddPointForTotalPointEvent?userId=&staminaBaseConsumption=&staminaConsumptionRatio=&mLiveSettingId=&isAutoPlay=&score=&achievementRatePercent=
@router.post(
    "/api/Debugs/AddPointForTotalPointEvent", name="Debug_AddPointForTotalPointEvent"
)
async def debug_add_point_for_total_point_event(
    request: Request,
    userId: Optional[int] = None,
    staminaBaseConsumption: Optional[int] = None,
    staminaConsumptionRatio: Optional[int] = None,
    mLiveSettingId: Optional[int] = None,
    isAutoPlay: Optional[bool] = None,
    score: Optional[int] = None,
    achievementRatePercent: Optional[str] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/AddRankPoint/{rankPoint}
@router.post("/api/Debugs/AddRankPoint/{rankPoint}", name="Debug_AddRankPoint")
async def debug_add_rank_point(request: Request, rankPoint: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/AddStarPoint/{mCharacterBaseId}/{amount}
@router.post(
    "/api/Debugs/AddStarPoint/{mCharacterBaseId}/{amount}", name="Debug_AddStarPoint"
)
async def debug_add_star_point(request: Request, mCharacterBaseId: int, amount: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(StarPointResult())


# /api/Debugs/AlbumSimpleArranging
@router.post("/api/Debugs/AlbumSimpleArranging", name="Debug_AlbumSimpleArranging")
async def debug_album_simple_arranging(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, DebugAlbumSimpleArrangingPayload)
    return respond(BooleanResult())


# /api/Debugs/AuthenticateOrRegister?userId=&hashedUserId=&gameVersion=
@router.post("/api/Debugs/AuthenticateOrRegister", name="Debug_AuthenticateOrRegister")
async def debug_authenticate_or_register(
    request: Request,
    userId: Optional[int] = None,
    hashedUserId: Optional[str] = None,
    gameVersion: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond("")


# /api/Debug/BattleGhost?mGhostLiveId=&uGhostUserId=&uPartyId=&score=
@router.post("/api/Debug/BattleGhost", name="Debug_BattleGhost")
async def debug_battle_ghost(
    request: Request,
    mGhostLiveId: Optional[int] = None,
    uGhostUserId: Optional[int] = None,
    uPartyId: Optional[int] = None,
    score: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/CallInboxService?isTimeLimited=&thingType=&thingId=&thingQuantity=&messageTemplateId=&message1=&message2=
@router.post("/api/Debugs/CallInboxService", name="Debug_CallInboxService")
async def debug_call_inbox_service(
    request: Request,
    isTimeLimited: Optional[bool] = None,
    thingType: Optional[int] = None,
    thingId: Optional[int] = None,
    thingQuantity: Optional[int] = None,
    messageTemplateId: Optional[int] = None,
    message1: Optional[str] = None,
    message2: Optional[str] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/CallInboxServiceMany?isTimeLimited=&thingType=&thingId=&thingQuantity=&count=&messageTemplateId=&message1=&message2=
@router.post("/api/Debugs/CallInboxServiceMany", name="Debug_CallInboxServiceMany")
async def debug_call_inbox_service_many(
    request: Request,
    isTimeLimited: Optional[bool] = None,
    thingType: Optional[int] = None,
    thingId: Optional[int] = None,
    thingQuantity: Optional[int] = None,
    count: Optional[int] = None,
    messageTemplateId: Optional[int] = None,
    message1: Optional[str] = None,
    message2: Optional[str] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/CircleUsageTimeReset?setDateTime=
@router.post("/api/Debugs/CircleUsageTimeReset", name="Debug_CircleUsageTimeReset")
async def debug_circle_usage_time_reset(
    request: Request, setDateTime: Optional[str] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/ClearAudition?toMAuditionId=&phase=
@router.post("/api/Debugs/ClearAudition", name="Debug_ClearAudition")
async def debug_clear_audition(
    request: Request, toMAuditionId: Optional[int] = None, phase: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debug/ClearBonusLiveEvent?bonusLiveMasterId=&clearStageOrder=
@router.post("/api/Debug/ClearBonusLiveEvent", name="Debug_ClearBonusLiveEvent")
async def debug_clear_bonus_live_event(
    request: Request,
    bonusLiveMasterId: Optional[int] = None,
    clearStageOrder: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debug/ClearTrialPartyEvent?trialPartyEventMasterId=&clearStageOrder=
@router.post("/api/Debug/ClearTrialPartyEvent", name="Debug_ClearTrialPartyEvent")
async def debug_clear_trial_party_event(
    request: Request,
    trialPartyEventMasterId: Optional[int] = None,
    clearStageOrder: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debug/ConvertMultiRoomId?uMultiRoomId=&hashedMultiRoomId=
@router.post("/api/Debug/ConvertMultiRoomId", name="Debug_ConvertMultiRoomId")
async def debug_convert_multi_room_id(
    request: Request,
    uMultiRoomId: Optional[int] = None,
    hashedMultiRoomId: Optional[str] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond("")


# /api/Debugs/CreateAlbum
@router.post("/api/Debugs/CreateAlbum", name="Debug_CreateAlbum")
async def debug_create_album(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/CreateCircleDummy/{startUserId}/{quantity}
@router.post(
    "/api/Debugs/CreateCircleDummy/{startUserId}/{quantity}",
    name="Debug_CreateCircleDummy",
)
async def debug_create_circle_dummy(request: Request, startUserId: int, quantity: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debug/CreateConcoursRandomRankings?mConcoursId=&count=
@router.post(
    "/api/Debug/CreateConcoursRandomRankings", name="Debug_CreateConcoursRandomRankings"
)
async def debug_create_concours_random_rankings(
    request: Request, mConcoursId: Optional[int] = None, count: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/CreateLeagueHistory?mLeagueId=&classType=&classChangeType=&groupRank=&globalRank=&isPlayed=&allClassGlobalRank=
@router.post("/api/Debugs/CreateLeagueHistory", name="Debug_CreateDummyLeagueHistory")
async def debug_create_dummy_league_history(
    request: Request,
    mLeagueId: Optional[int] = None,
    classType: Optional[int] = None,
    classChangeType: Optional[int] = None,
    groupRank: Optional[int] = None,
    globalRank: Optional[int] = None,
    isPlayed: Optional[bool] = None,
    allClassGlobalRank: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/CreateDummyUsers?userCount=
@router.post("/api/Debugs/CreateDummyUsers", name="Debug_CreateDummyUsers")
async def debug_create_dummy_users(request: Request, userCount: Optional[int] = None):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])


# /api/Debugs/CreateFriendRequestForMe/{count}
@router.post(
    "/api/Debugs/CreateFriendRequestForMe/{count}",
    name="Debug_CreateFriendRequestForMe",
)
async def debug_create_friend_request_for_me(request: Request, count: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/CreateTripleCastHistory?mTripleCastId=&classType=&classChangeType=&groupRank=&globalRank=&isPlayed=&allClassGlobalRank=
@router.post(
    "/api/Debugs/CreateTripleCastHistory", name="Debug_CreateTripleCastHistory"
)
async def debug_create_triple_cast_history(
    request: Request,
    mTripleCastId: Optional[int] = None,
    classType: Optional[int] = None,
    classChangeType: Optional[int] = None,
    groupRank: Optional[int] = None,
    globalRank: Optional[int] = None,
    isPlayed: Optional[bool] = None,
    allClassGlobalRank: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/Circle/SupportPoint/DailyAddedSupportPoint/{point}
@router.post(
    "/api/Debugs/Circle/SupportPoint/DailyAddedSupportPoint/{point}",
    name="Debug_DailyAddedSupportPoint",
)
async def debug_daily_added_support_point(request: Request, point: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/DeleteAllCourseRanking?musicCourseMasterId=
@router.post("/api/Debugs/DeleteAllCourseRanking", name="Debug_DeleteAllCourseRanking")
async def debug_delete_all_course_ranking(
    request: Request, musicCourseMasterId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/DeleteCircles
@router.post("/api/Debugs/DeleteCircles", name="Debug_DeleteCircles")
async def debug_delete_circles(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/DeleteLeagueAllData
@router.post("/api/Debugs/DeleteLeagueAllData", name="Debug_DeleteLeagueAllData")
async def debug_delete_league_all_data(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/DeleteLeagueData/{mLeagueId}
@router.post("/api/Debugs/DeleteLeagueData/{mLeagueId}", name="Debug_DeleteLeagueData")
async def debug_delete_league_data(request: Request, mLeagueId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/DeleteLeagueUserData/{userId}
@router.post(
    "/api/Debugs/DeleteLeagueUserData/{userId}", name="Debug_DeleteLeagueUserData"
)
async def debug_delete_league_user_data(request: Request, userId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/DeleteLeagueUsersData
@router.post("/api/Debugs/DeleteLeagueUsersData", name="Debug_DeleteLeagueUsersData")
async def debug_delete_league_users_data(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request)
    return respond(BooleanResult())


# /api/Debugs/DeleteTripleCastData/{mTripleCastId}
@router.post(
    "/api/Debugs/DeleteTripleCastData/{mTripleCastId}",
    name="Debug_DeleteTripleCastData",
)
async def debug_delete_triple_cast_data(request: Request, mTripleCastId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/EasyStartLive?mMusicId=&difficulty=
@router.post("/api/Debugs/EasyStartLive", name="Debug_EasyStartLive")
async def debug_easy_start_live(
    request: Request, mMusicId: Optional[int] = None, difficulty: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/EditLeagueBasic
@router.post("/api/Debugs/EditLeagueBasic", name="Debug_EditLeagueBasic")
async def debug_edit_league_basic(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, DebugEditLeagueBasicPayload)
    return respond(BooleanResult())


# /api/Debugs/EditLeagueHistory?mLeagueId=&classType=&classChangeType=&groupRank=&globalRank=&receivedReward=
@router.post("/api/Debugs/EditLeagueHistory", name="Debug_EditLeagueHistory")
async def debug_edit_league_history(
    request: Request,
    mLeagueId: Optional[int] = None,
    classType: Optional[int] = None,
    classChangeType: Optional[int] = None,
    groupRank: Optional[int] = None,
    globalRank: Optional[int] = None,
    receivedReward: Optional[bool] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/ExecuteLeagueTotalization
@router.post(
    "/api/Debugs/ExecuteLeagueTotalization", name="Debug_ExecuteLeagueTotalization"
)
async def debug_execute_league_totalization(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/FinishLive?remainedLife=
@router.post("/api/Debugs/FinishLive", name="Debug_FinishLive")
async def debug_finish_live(request: Request, remainedLife: Optional[int] = None):
    app: YumeApp = request.app
    payload = await read_request(request, FinishLivePayload)
    return respond(FinishLiveResult())


# /api/Debugs/FinishLiveSpecifiedNotes?score=&perfectStar=&perfect=&great=&good=&bad=&miss=&remainedLife=&maxCombo=&isClear=
@router.post(
    "/api/Debugs/FinishLiveSpecifiedNotes", name="Debug_FinishLiveSpecifiedNotes"
)
async def debug_finish_live_specified_notes(
    request: Request,
    score: Optional[int] = None,
    perfectStar: Optional[int] = None,
    perfect: Optional[int] = None,
    great: Optional[int] = None,
    good: Optional[int] = None,
    bad: Optional[int] = None,
    miss: Optional[int] = None,
    remainedLife: Optional[int] = None,
    maxCombo: Optional[int] = None,
    isClear: Optional[bool] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(FinishLiveResult())


# /api/Debugs/GenerateCharacterPointEventPointRanking/{mCharacterPointEventId}
@router.post(
    "/api/Debugs/GenerateCharacterPointEventPointRanking/{mCharacterPointEventId}",
    name="Debug_GenerateCharacterPointEventPointRanking",
)
async def debug_generate_character_point_event_point_ranking(
    request: Request, mCharacterPointEventId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/GenerateDummyCharacterPointEventPointRanking/{mCharacterPointEventId}/{amount}/{maxPoint}?mCharacterBaseId=&diff=
@router.post(
    "/api/Debugs/GenerateDummyCharacterPointEventPointRanking/{mCharacterPointEventId}/{amount}/{maxPoint}",
    name="Debug_GenerateDummyCharacterPointEventPointRanking",
)
async def debug_generate_dummy_character_point_event_point_ranking(
    request: Request,
    mCharacterPointEventId: int,
    amount: int,
    maxPoint: int,
    mCharacterBaseId: Optional[int] = None,
    diff: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/GenerateDummyTotalPointEventPointRanking/{mTotalPointEventId}/{amount}/{maxPoint}?diff=
@router.post(
    "/api/Debugs/GenerateDummyTotalPointEventPointRanking/{mTotalPointEventId}/{amount}/{maxPoint}",
    name="Debug_GenerateDummyTotalPointEventPointRanking",
)
async def debug_generate_dummy_total_point_event_point_ranking(
    request: Request,
    mTotalPointEventId: int,
    amount: int,
    maxPoint: int,
    diff: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/GenerateLeagueGroupScore?mLeagueId=&minScore=&maxScore=
@router.post(
    "/api/Debugs/GenerateLeagueGroupScore", name="Debug_GenerateLeagueGroupScore"
)
async def debug_generate_league_group_score(
    request: Request,
    mLeagueId: Optional[int] = None,
    minScore: Optional[int] = None,
    maxScore: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/GenerateLinkageCodeAndPassword?userId=&hashedUserId=
@router.post(
    "/api/Debugs/GenerateLinkageCodeAndPassword",
    name="Debug_GenerateLinkageCodeAndPassword",
)
async def debug_generate_linkage_code_and_password(
    request: Request, userId: Optional[int] = None, hashedUserId: Optional[str] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(DebugLinkageCodeResult())


# /api/Debugs/GenerateLiveRate/{count}/{achievementRate}
@router.post(
    "/api/Debugs/GenerateLiveRate/{count}/{achievementRate}",
    name="Debug_GenerateLiveRate",
)
async def debug_generate_live_rate(request: Request, count: int, achievementRate: str):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debug/GenerateLotteryResult?mLotteryId=
@router.post("/api/Debug/GenerateLotteryResult", name="Debug_GenerateLotteryResult")
async def debug_generate_lottery_result(
    request: Request, mLotteryId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = await read_request(request, GenerateLotteryResultPayload)
    return respond(BooleanResult())


# /api/Debugs/GenerateStoryEventHighScoreRanking?mStoryEventId=
@router.post(
    "/api/Debugs/GenerateStoryEventHighScoreRanking",
    name="Debug_GenerateStoryEventHighScoreRanking",
)
async def debug_generate_story_event_high_score_ranking(
    request: Request, mStoryEventId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/GenerateStoryEventPointRanking?mStoryEventId=
@router.post(
    "/api/Debugs/GenerateStoryEventPointRanking",
    name="Debug_GenerateStoryEventPointRanking",
)
async def debug_generate_story_event_point_ranking(
    request: Request, mStoryEventId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/CacheUpdatedAt
@router.get("/api/Debugs/CacheUpdatedAt", name="Debug_GetCacheUpdatedAt")
async def debug_get_cache_updated_at(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond("")


# /api/Debugs/GetToken?userId=&hashedUserId=&gameVersion=
@router.post("/api/Debugs/GetToken", name="Debug_GetCurrentApiToken")
async def debug_get_current_api_token(
    request: Request,
    userId: Optional[int] = None,
    hashedUserId: Optional[str] = None,
    gameVersion: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond("")


# /api/Debugs/GetCurrentLeague
@router.get("/api/Debugs/GetCurrentLeague", name="Debug_GetCurrentLeague")
async def debug_get_current_league(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(0)


# /api/Debugs/GetEpisode?episodeMasterId=
@router.post("/api/Debugs/GetEpisode", name="Debug_GetEpisode")
async def debug_get_episode(request: Request, episodeMasterId: Optional[int] = None):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(EpisodeResult())


# /api/Debugs/GetLeagueHistories
@router.get("/api/Debugs/GetLeagueHistories", name="Debug_GetLeagueHistories")
async def debug_get_league_histories(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond("")


# /api/Debugs/LiveScoreHistory
@router.get("/api/Debugs/LiveScoreHistory", name="Debug_GetLiveScoreHistory")
async def debug_get_live_score_history(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([ScoreWithDateResult()])


# /api/Debugs/ConvertUserId?userId=&hashedUserId=
@router.post("/api/Debugs/ConvertUserId", name="Debug_GetUsetId")
async def debug_get_uset_id(
    request: Request, userId: Optional[str] = None, hashedUserId: Optional[str] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(DebugUserIdResult())


# /api/Debugs/GiveEnhanceItems
@router.post("/api/Debugs/GiveEnhanceItems", name="Debug_GiveEnhanceItems")
async def debug_give_enhance_items(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/GrowAccessoriesMax
@router.post(
    "/api/Debugs/GrowAccessoriesMax", name="Debug_GiveEnhanceItemsAndGrowAccessoriesMax"
)
async def debug_give_enhance_items_and_grow_accessories_max(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/GiveEnhanceItemsAndGrowCharactersMax
@router.post(
    "/api/Debugs/GiveEnhanceItemsAndGrowCharactersMax",
    name="Debug_GiveEnhanceItemsAndGrowCharactersMax",
)
async def debug_give_enhance_items_and_grow_characters_max(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/GiveEnhanceItemsAndGrowPostersMax
@router.post(
    "/api/Debugs/GiveEnhanceItemsAndGrowPostersMax",
    name="Debug_GiveEnhanceItemsAndGrowPostersMax",
)
async def debug_give_enhance_items_and_grow_posters_max(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/Yokubari
@router.post("/api/Debugs/Yokubari", name="Debug_GrantAllThing")
async def debug_grant_all_thing(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/InitializeLeagueBasicData
@router.post(
    "/api/Debugs/InitializeLeagueBasicData", name="Debug_InitializeLeagueBasicData"
)
async def debug_initialize_league_basic_data(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/InitializePlayerRate
@router.post("/api/Debugs/InitializePlayerRate", name="Debug_InitializePlayerRate")
async def debug_initialize_player_rate(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/JoinOrCreateLeagueGroupMember?mLeagueId=
@router.post(
    "/api/Debugs/JoinOrCreateLeagueGroupMember",
    name="Debug_JoinOnCreateLeagueGroupMember",
)
async def debug_join_on_create_league_group_member(
    request: Request, mLeagueId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/LeaveLeagueGroup?mLeagueId=
@router.post("/api/Debugs/LeaveLeagueGroup", name="Debug_LeaveLeagueGroup")
async def debug_leave_league_group(request: Request, mLeagueId: Optional[int] = None):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/OpenAllFlashSale?isDefault=
@router.post("/api/Debugs/OpenAllFlashSale", name="Debug_OpenAllFalshSale")
async def debug_open_all_falsh_sale(request: Request, isDefault: Optional[bool] = None):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/PrepareLeagueGroupUser
@router.post("/api/Debugs/PrepareLeagueGroupUser", name="Debug_PrepareLeagueGroupUser")
async def debug_prepare_league_group_user(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, DebugPrepareLeagueGroupUserPayload)
    return respond(BooleanResult())


# /api/Debugs/PurchaseDaiStarPass?lastEnabled=&totalPurchasedCount=
@router.post("/api/Debugs/PurchaseDaiStarPass", name="Debug_PurchaseDaiStarPass")
async def debug_purchase_dai_star_pass(
    request: Request,
    lastEnabled: Optional[str] = None,
    totalPurchasedCount: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debug/PurchaseExternalPaymentItem?mJewelShopItemId=
@router.post(
    "/api/Debug/PurchaseExternalPaymentItem", name="Debug_PurchaseExternalPaymentItem"
)
async def debug_purchase_external_payment_item(
    request: Request, mJewelShopItemId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/PurchaseStarPass?lastEnabled=&totalPurchasedCount=
@router.post("/api/Debugs/PurchaseStarPass", name="Debug_PurchaseStarPass")
async def debug_purchase_star_pass(
    request: Request,
    lastEnabled: Optional[str] = None,
    totalPurchasedCount: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debug/ReadRequiredEpisode?episodeMasterId=
@router.post("/api/Debug/ReadRequiredEpisode", name="Debug_ReadRequiredEpisode")
async def debug_read_required_episode(
    request: Request, episodeMasterId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/RecordActivityLog?logType=&logValue=
@router.post("/api/Debugs/RecordActivityLog", name="Debug_RecordActivityLog")
async def debug_record_activity_log(
    request: Request, logType: Optional[int] = None, logValue: Optional[str] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SetLeagueDaistarEnrollCount/{enrollCount}
@router.post(
    "/api/Debugs/SetLeagueDaistarEnrollCount/{enrollCount}",
    name="Debug_ReestCircleEventPointAndMission",
)
async def debug_reest_circle_event_point_and_mission(
    request: Request, enrollCount: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/CircleEvent/ReestCirclePointAndMission/{mCircleEventId}
@router.post(
    "/api/Debugs/CircleEvent/ReestCirclePointAndMission/{mCircleEventId}",
    name="Debug_ReestCircleEventPointAndMission2",
)
async def debug_reest_circle_event_point_and_mission2(
    request: Request, mCircleEventId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/RefreshMemoryCache
@router.get("/api/Debugs/RefreshMemoryCache", name="Debug_RefreshMemoryCache")
async def debug_refresh_memory_cache(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/ReleaseAllEpisodes/{timesRead}
@router.post(
    "/api/Debugs/ReleaseAllEpisodes/{timesRead}", name="Debug_ReleaseAllEpisodes"
)
async def debug_release_all_episodes(request: Request, timesRead: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/ReleaseAllMusicDifficulty
@router.post(
    "/api/Debugs/ReleaseAllMusicDifficulty", name="Debug_ReleaseAllMusicDifficulty"
)
async def debug_release_all_music_difficulty(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/ResetAutoPlay
@router.post("/api/Debugs/ResetAutoPlay", name="Debug_ResetAutoPlay")
async def debug_reset_auto_play(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debug/ResetCampEventSupportPointRanking?mEventId=
@router.post(
    "/api/Debug/ResetCampEventSupportPointRanking",
    name="Debug_ResetCampEventSupportPointRanking",
)
async def debug_reset_camp_event_support_point_ranking(
    request: Request, mEventId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/ResetCharacterPointEventPointRanking/{mCharacterPointEventId}
@router.post(
    "/api/Debugs/ResetCharacterPointEventPointRanking/{mCharacterPointEventId}",
    name="Debug_ResetCharacterPointEventPointRanking",
)
async def debug_reset_character_point_event_point_ranking(
    request: Request, mCharacterPointEventId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debug/ResetEventPointRanking?mEventId=
@router.post("/api/Debug/ResetEventPointRanking", name="Debug_ResetEventPointRanking")
async def debug_reset_event_point_ranking(
    request: Request, mEventId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/ResetLesson
@router.post("/api/Debugs/ResetLesson", name="Debug_ResetLesson")
async def debug_reset_lesson(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debug/ResetPickupGachaSelectedThings?gachaMasterId=
@router.post(
    "/api/Debug/ResetPickupGachaSelectedThings",
    name="Debug_ResetPickupGachaSelectedThings",
)
async def debug_reset_pickup_gacha_selected_things(
    request: Request, gachaMasterId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = await read_request(request, SetSelectedThingsPayload)
    return respond(BooleanResult())


# /api/Debugs/ResetStoryEventHighScoreRanking?mStoryEventId=
@router.post(
    "/api/Debugs/ResetStoryEventHighScoreRanking",
    name="Debug_ResetStoryEventHighScoreRanking",
)
async def debug_reset_story_event_high_score_ranking(
    request: Request, mStoryEventId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/ResetStoryEventPointRanking?mStoryEventId=
@router.post(
    "/api/Debugs/ResetStoryEventPointRanking", name="Debug_ResetStoryEventPointRanking"
)
async def debug_reset_story_event_point_ranking(
    request: Request, mStoryEventId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/ResetTotalPointEvent?mTotalPointEvent=
@router.post("/api/Debugs/ResetTotalPointEvent", name="Debug_ResetTotalPointEvent")
async def debug_reset_total_point_event(
    request: Request, mTotalPointEvent: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SendAccessories
@router.post("/api/Debugs/SendAccessories", name="Debug_SendAccessories")
async def debug_send_accessories(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request)
    return respond(BooleanResult())


# /api/Debugs/SendAccessoryWithEffect?mAccessoryId=&level=&mAccessoryEffectId1=&mAccessoryEffectId2=&mAccessoryEffectId3=
@router.post(
    "/api/Debugs/SendAccessoryWithEffect", name="Debug_SendAccessoryWithEffect"
)
async def debug_send_accessory_with_effect(
    request: Request,
    mAccessoryId: Optional[int] = None,
    level: Optional[int] = None,
    mAccessoryEffectId1: Optional[int] = None,
    mAccessoryEffectId2: Optional[int] = None,
    mAccessoryEffectId3: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SendAlbumThemes
@router.post("/api/Debugs/SendAlbumThemes", name="Debug_SendAlbuThemes")
async def debug_send_albu_themes(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request)
    return respond(BooleanResult())


# /api/Debugs/SendAlbumTheme/{mAlbumThemeId}
@router.post("/api/Debugs/SendAlbumTheme/{mAlbumThemeId}", name="Debug_SendAlbumTheme")
async def debug_send_album_theme(request: Request, mAlbumThemeId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SendBomb/{mBombId}
@router.post("/api/Debugs/SendBomb/{mBombId}", name="Debug_SendBomb")
async def debug_send_bomb(request: Request, mBombId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SendBombs
@router.post("/api/Debugs/SendBombs", name="Debug_SendBombs")
async def debug_send_bombs(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request)
    return respond(BooleanResult())


# /api/Debugs/SendCharacter/{mCharacterId}/{quantity}
@router.post(
    "/api/Debugs/SendCharacter/{mCharacterId}/{quantity}", name="Debug_SendCharacter"
)
async def debug_send_character(request: Request, mCharacterId: int, quantity: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SendCharacters
@router.post("/api/Debugs/SendCharacters", name="Debug_SendCharacters")
async def debug_send_characters(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, AcquirableThingsPayload)
    return respond(BooleanResult())


# /api/Debugs/SendChatworkMessage
@router.post("/api/Debugs/SendChatworkMessage", name="Debug_SendChatworkMessage")
async def debug_send_chatwork_message(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, ChatworkSendMessagePayload)
    return respond(BooleanResult())


# /api/Debugs/SendCoin/{amount}?isPaid=
@router.post("/api/Debugs/SendCoin/{amount}", name="Debug_SendCoin")
async def debug_send_coin(request: Request, amount: int, isPaid: Optional[bool] = None):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SendCostume/{mCostumeId}
@router.post("/api/Debugs/SendCostume/{mCostumeId}", name="Debug_SendCostume")
async def debug_send_costume(request: Request, mCostumeId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SendCostumes
@router.post("/api/Debugs/SendCostumes", name="Debug_SendCostumes")
async def debug_send_costumes(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request)
    return respond(BooleanResult())


# /api/Debugs/SendDecoration/{mDecorationId}
@router.post("/api/Debugs/SendDecoration/{mDecorationId}", name="Debug_SendDecoration")
async def debug_send_decoration(request: Request, mDecorationId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SendDecorations
@router.post("/api/Debugs/SendDecorations", name="Debug_SendDecorations")
async def debug_send_decorations(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request)
    return respond(BooleanResult())


# /api/Debug/SendHomeSkin?mHomeSkinId=
@router.post("/api/Debug/SendHomeSkin", name="Debug_SendHomeSkin")
async def debug_send_home_skin(request: Request, mHomeSkinId: Optional[int] = None):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SendHomeSkins
@router.post("/api/Debugs/SendHomeSkins", name="Debug_SendHomeSkins")
async def debug_send_home_skins(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request)
    return respond(BooleanResult())


# /api/Debug/SendIconFrame?mIconFrameId=&mAlbumThemeId=
@router.post("/api/Debug/SendIconFrame", name="Debug_SendIconFrame")
async def debug_send_icon_frame(
    request: Request,
    mIconFrameId: Optional[int] = None,
    mAlbumThemeId: Optional[str] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SendIconFrames
@router.post("/api/Debugs/SendIconFrames", name="Debug_SendIconFrames")
async def debug_send_icon_frames(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request)
    return respond(BooleanResult())


# /api/Debugs/SendItem/{mItemId}/{quantity}
@router.post("/api/Debugs/SendItem/{mItemId}/{quantity}", name="Debug_SendItem")
async def debug_send_item(request: Request, mItemId: int, quantity: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SendItems
@router.post("/api/Debugs/SendItems", name="Debug_SendItems")
async def debug_send_items(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, AcquirableThingsPayload)
    return respond(BooleanResult())


# /api/Debugs/SendJewel/{amount}
@router.post("/api/Debugs/SendJewel/{amount}", name="Debug_SendJewel")
async def debug_send_jewel(request: Request, amount: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SendLoginBonusAgain?mLoginBonusId=&currentLoginCount=
@router.post("/api/Debugs/SendLoginBonusAgain", name="Debug_SendLoginBonusAgain")
async def debug_send_login_bonus_again(
    request: Request,
    mLoginBonusId: Optional[int] = None,
    currentLoginCount: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SendMusic/{mMusicId}
@router.post("/api/Debugs/SendMusic/{mMusicId}", name="Debug_SendMusic")
async def debug_send_music(request: Request, mMusicId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SendMusics
@router.post("/api/Debugs/SendMusics", name="Debug_SendMusics")
async def debug_send_musics(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request)
    return respond(BooleanResult())


# /api/Debug/SendNameBaseColor?mNameBaseColorId=&mAlbumThemeId=
@router.post("/api/Debug/SendNameBaseColor", name="Debug_SendNameBaseColor")
async def debug_send_name_base_color(
    request: Request,
    mNameBaseColorId: Optional[int] = None,
    mAlbumThemeId: Optional[str] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SendNameBaseColors
@router.post("/api/Debugs/SendNameBaseColors", name="Debug_SendNameBaseColors")
async def debug_send_name_base_colors(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request)
    return respond(BooleanResult())


# /api/Debugs/SendNameColor/{mNameColorId}
@router.post("/api/Debugs/SendNameColor/{mNameColorId}", name="Debug_SendNameColor")
async def debug_send_name_color(request: Request, mNameColorId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SendNameColors
@router.post("/api/Debugs/SendNameColors", name="Debug_SendNameColors")
async def debug_send_name_colors(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request)
    return respond(BooleanResult())


# /api/Debugs/SendNameplate/{mNamePlateId}
@router.post("/api/Debugs/SendNameplate/{mNamePlateId}", name="Debug_SendNameplate")
async def debug_send_nameplate(request: Request, mNamePlateId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SendNameplates
@router.post("/api/Debugs/SendNameplates", name="Debug_SendNameplates")
async def debug_send_nameplates(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request)
    return respond(BooleanResult())


# /api/Debugs/SendNote/{mNoteId}
@router.post("/api/Debugs/SendNote/{mNoteId}", name="Debug_SendNote")
async def debug_send_note(request: Request, mNoteId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SendNotes
@router.post("/api/Debugs/SendNotes", name="Debug_SendNotes")
async def debug_send_notes(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request)
    return respond(BooleanResult())


# /api/Debugs/SendNotification
@router.post("/api/Debugs/SendNotification", name="Debug_SendNotification")
async def debug_send_notification(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SendPaidJewel/{amount}
@router.post("/api/Debugs/SendPaidJewel/{amount}", name="Debug_SendPaidJewel")
async def debug_send_paid_jewel(request: Request, amount: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SendPoster/{mPosterId}/{quantity}
@router.post("/api/Debugs/SendPoster/{mPosterId}/{quantity}", name="Debug_SendPoster")
async def debug_send_poster(request: Request, mPosterId: int, quantity: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SendPosters
@router.post("/api/Debugs/SendPosters", name="Debug_SendPosters")
async def debug_send_posters(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, AcquirableThingsPayload)
    return respond(BooleanResult())


# /api/Debugs/SendStamps
@router.post("/api/Debugs/SendStamps", name="Debug_SendStamp")
async def debug_send_stamp(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request)
    return respond(BooleanResult())


# /api/Debugs/SendStamp/{mStampId}
@router.post("/api/Debugs/SendStamp/{mStampId}", name="Debug_SendStamp2")
async def debug_send_stamp2(request: Request, mStampId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SendTrophies
@router.post("/api/Debugs/SendTrophies", name="Debug_SendTrophies")
async def debug_send_trophies(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request)
    return respond(BooleanResult())


# /api/Debugs/SendTrophy/{mTrophyId}
@router.post("/api/Debugs/SendTrophy/{mTrophyId}", name="Debug_SendTrophy")
async def debug_send_trophy(request: Request, mTrophyId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SetAutoPlayAvailableTimes/{times}
@router.post(
    "/api/Debugs/SetAutoPlayAvailableTimes/{times}",
    name="Debug_SetAutoPlayAvailableTimes",
)
async def debug_set_auto_play_available_times(request: Request, times: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SetCharacterEnhanceInfo
@router.post(
    "/api/Debugs/SetCharacterEnhanceInfo", name="Debug_SetCharacterEnhanceInfo"
)
async def debug_set_character_enhance_info(request: Request):
    app: YumeApp = request.app
    payload = await read_request(
        request, "DebugModifyCharacterEnhanceInformationPayload"
    )
    return respond(BooleanResult())


# /api/Debugs/SetCharacterMissionCount/{characterBaseMasterId}/{characterMissionMasterId}/{count}
@router.post(
    "/api/Debugs/SetCharacterMissionCount/{characterBaseMasterId}/{characterMissionMasterId}/{count}",
    name="Debug_SetCharacterMissionCount",
)
async def debug_set_character_mission_count(
    request: Request,
    characterBaseMasterId: int,
    characterMissionMasterId: int,
    count: int,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SetCharacterPointEventPoint/{mCharacterPointEventId}/{amount}
@router.post(
    "/api/Debugs/SetCharacterPointEventPoint/{mCharacterPointEventId}/{amount}",
    name="Debug_SetCharacterPointEventPoint",
)
async def debug_set_character_point_event_point(
    request: Request, mCharacterPointEventId: int, amount: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/Circle/SupportPoint/{company}?level=&point=&lastLevelupDate=&levelLimit=
@router.post(
    "/api/Debugs/Circle/SupportPoint/{company}", name="Debug_SetCircleSupportPointInfo"
)
async def debug_set_circle_support_point_info(
    request: Request,
    company: int,
    level: Optional[int] = None,
    point: Optional[int] = None,
    lastLevelupDate: Optional[str] = None,
    levelLimit: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/Circle/SupportCompanyLevelLimit
@router.post(
    "/api/Debugs/Circle/SupportCompanyLevelLimit",
    name="Debug_SetCircleSupportPointInfo2",
)
async def debug_set_circle_support_point_info2(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, SupportCompanyLevelLimitPayload)
    return respond(BooleanResult())


# /api/Debugs/SetCourseRankingResultsDecreasingByPercent?musicCourseMasterId=
@router.post(
    "/api/Debugs/SetCourseRankingResultsDecreasingByPercent",
    name="Debug_SetCourseRankingResultsDecreasingByPercent",
)
async def debug_set_course_ranking_results_decreasing_by_percent(
    request: Request, musicCourseMasterId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debug/SetEventPoint?mEventId=&amount=
@router.post("/api/Debug/SetEventPoint", name="Debug_SetEventPoint")
async def debug_set_event_point(
    request: Request, mEventId: Optional[int] = None, amount: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SetFlashSaleCount?mFlashSaleId=&count=&isDefault=
@router.post("/api/Debugs/SetFlashSaleCount", name="Debug_SetFlashSaleCount")
async def debug_set_flash_sale_count(
    request: Request,
    mFlashSaleId: Optional[int] = None,
    count: Optional[int] = None,
    isDefault: Optional[bool] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debug/SetGhost?mGhostLiveId=&uPartyId=&score=
@router.post("/api/Debug/SetGhost", name="Debug_SetGhost")
async def debug_set_ghost(
    request: Request,
    mGhostLiveId: Optional[int] = None,
    uPartyId: Optional[int] = None,
    score: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debug/SetGingaTheaterLiveDropLimit?multiLiveScheduleMasterId=&setCurrentCount=
@router.post(
    "/api/Debug/SetGingaTheaterLiveDropLimit", name="Debug_SetGingaTheaterLiveDropLimit"
)
async def debug_set_ginga_theater_live_drop_limit(
    request: Request,
    multiLiveScheduleMasterId: Optional[int] = None,
    setCurrentCount: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debug/SetLeagueGroupScore?leagueMasterId=&startScore=
@router.post("/api/Debug/SetLeagueGroupScore", name="Debug_SetLeagueGroupScore")
async def debug_set_league_group_score(
    request: Request,
    leagueMasterId: Optional[int] = None,
    startScore: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SetLeagueScore?mLeagueId=&score=
@router.post("/api/Debugs/SetLeagueScore", name="Debug_SetLeagueScore")
async def debug_set_league_score(
    request: Request, mLeagueId: Optional[int] = None, score: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SetLoginPassUntil?until=
@router.post("/api/Debugs/SetLoginPassUntil", name="Debug_SetLoginPassUntil")
async def debug_set_login_pass_until(request: Request, until: Optional[str] = None):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SetMarketFrameThing?number=&mMarketFrameThingId=
@router.post("/api/Debugs/SetMarketFrameThing", name="Debug_SetMarketFrameThing")
async def debug_set_market_frame_thing(
    request: Request,
    number: Optional[int] = None,
    mMarketFrameThingId: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SetMissionCount/{mMissionId}/{count}
@router.post(
    "/api/Debugs/SetMissionCount/{mMissionId}/{count}", name="Debug_SetMissionCount"
)
async def debug_set_mission_count(request: Request, mMissionId: int, count: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SetMusicCourseRanking?musicCourseMasterId=
@router.post("/api/Debugs/SetMusicCourseRanking", name="Debug_SetMusicCourseRanking")
async def debug_set_music_course_ranking(
    request: Request, musicCourseMasterId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = await read_request(request, MusicCourseRankingPayload)
    return respond(BooleanResult())


# /api/Debugs/SetParty?uPartyId=
@router.post("/api/Debugs/SetParty", name="Debug_SetParty")
async def debug_set_party(request: Request, uPartyId: Optional[int] = None):
    app: YumeApp = request.app
    payload = await read_request(request, PartyPayload)
    return respond(BooleanResult())


# /api/Debugs/SetPhoto?mPhotoEffectId=&isLock=&level=&rarity=&mSignId=
@router.post("/api/Debugs/SetPhoto", name="Debug_SetPhoto")
async def debug_set_photo(
    request: Request,
    mPhotoEffectId: Optional[int] = None,
    isLock: Optional[bool] = None,
    level: Optional[int] = None,
    rarity: Optional[int] = None,
    mSignId: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SetPlayerRankWithPoint/{rank}
@router.post(
    "/api/Debugs/SetPlayerRankWithPoint/{rank}", name="Debug_SetPlayerRankWithPoint"
)
async def debug_set_player_rank_with_point(request: Request, rank: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SetPlayerRate?rate=
@router.post("/api/Debugs/SetPlayerRate", name="Debug_SetPlayerRate")
async def debug_set_player_rate(request: Request, rate: Optional[str] = None):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SetPosterEnhanceInfo
@router.post("/api/Debugs/SetPosterEnhanceInfo", name="Debug_SetPosterEnhanceInfo")
async def debug_set_poster_enhance_info(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, DebugModifyPosterEnhanceInformationPayload)
    return respond(BooleanResult())


# /api/Debugs/SetReleasableOlivier/{mMusicId}/{releasableOlivier}
@router.post(
    "/api/Debugs/SetReleasableOlivier/{mMusicId}/{releasableOlivier}",
    name="Debug_SetReleasableOlivier",
)
async def debug_set_releasable_olivier(
    request: Request, mMusicId: int, releasableOlivier: bool
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SetReleasedStella/{mMusicId}/{releasedStella}
@router.post(
    "/api/Debugs/SetReleasedStella/{mMusicId}/{releasedStella}",
    name="Debug_SetReleasedStella",
)
async def debug_set_released_stella(
    request: Request, mMusicId: int, releasedStella: bool
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SetServerTime?dateTime=
@router.post("/api/Debugs/SetServerTime", name="Debug_SetServerTime")
async def debug_set_server_time(request: Request, dateTime: Optional[str] = None):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SetSpRate/{mMusicId}/{point}
@router.post("/api/Debugs/SetSpRate/{mMusicId}/{point}", name="Debug_SetSpRate")
async def debug_set_sp_rate(request: Request, mMusicId: int, point: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debug/SetSpRatePoint?point=
@router.post("/api/Debug/SetSpRatePoint", name="Debug_SetSpRatePoint")
async def debug_set_sp_rate_point(request: Request, point: Optional[int] = None):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debug/SetSpRateSegment?segment=
@router.post("/api/Debug/SetSpRateSegment", name="Debug_SetSpRateSegment")
async def debug_set_sp_rate_segment(request: Request, segment: Optional[int] = None):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SetSplashLastDisplayedAt?displayedAtText=
@router.post(
    "/api/Debugs/SetSplashLastDisplayedAt", name="Debug_SetSplashLastDisplayedAt"
)
async def debug_set_splash_last_displayed_at(
    request: Request, displayedAtText: Optional[str] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SetStamina/{stamina}
@router.post("/api/Debugs/SetStamina/{stamina}", name="Debug_SetStamina")
async def debug_set_stamina(request: Request, stamina: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/Circle/SupportPoint/StaminaLastReceivedAt/{lastReceivedAt}
@router.post(
    "/api/Debugs/Circle/SupportPoint/StaminaLastReceivedAt/{lastReceivedAt}",
    name="Debug_SetStaminaLastReceivedAt",
)
async def debug_set_stamina_last_received_at(request: Request, lastReceivedAt: str):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SetStarRank/{mCharacterBaseId}/{rank}
@router.post(
    "/api/Debugs/SetStarRank/{mCharacterBaseId}/{rank}", name="Debug_SetStarRank"
)
async def debug_set_star_rank(request: Request, mCharacterBaseId: int, rank: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SetStoryEventHighScoreEnhancementPoint?mStoryEventId=&currentPoint=&totalAcquiredPoint=
@router.post(
    "/api/Debugs/SetStoryEventHighScoreEnhancementPoint",
    name="Debug_SetStoryEventHighScoreEnhancementPoint",
)
async def debug_set_story_event_high_score_enhancement_point(
    request: Request,
    mStoryEventId: Optional[int] = None,
    currentPoint: Optional[int] = None,
    totalAcquiredPoint: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SetStoryEventPoint/{mStoryEventId}/{amount}
@router.post(
    "/api/Debugs/SetStoryEventPoint/{mStoryEventId}/{amount}",
    name="Debug_SetStoryEventPoint",
)
async def debug_set_story_event_point(
    request: Request, mStoryEventId: int, amount: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SetTimeWarpByDate?setDateTime=
@router.post("/api/Debugs/SetTimeWarpByDate", name="Debug_SetTimeWarpByDate")
async def debug_set_time_warp_by_date(
    request: Request, setDateTime: Optional[str] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SetTimeWarpBySpecifyOffset?addDays=&addHours=&addMinutes=
@router.post(
    "/api/Debugs/SetTimeWarpBySpecifyOffset", name="Debug_SetTimeWarpBySpecifyOffset"
)
async def debug_set_time_warp_by_specify_offset(
    request: Request,
    addDays: Optional[int] = None,
    addHours: Optional[int] = None,
    addMinutes: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SetTotalPointEvent?mTotalPointEventId=&totalPoint=
@router.post("/api/Debugs/SetTotalPointEvent", name="Debug_SetTotalPointEvent")
async def debug_set_total_point_event(
    request: Request,
    mTotalPointEventId: Optional[int] = None,
    totalPoint: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SetTournamentDetail/{tournamentDetailMasterId}?mTournamentDetailMasterId=&perfectStar=&perfect=&great=&good=&bad=&miss=
@router.post(
    "/api/Debugs/SetTournamentDetail/{tournamentDetailMasterId}",
    name="Debug_SetTournamentDetail",
)
async def debug_set_tournament_detail(
    request: Request,
    tournamentDetailMasterId: str,
    mTournamentDetailMasterId: Optional[int] = None,
    perfectStar: Optional[int] = None,
    perfect: Optional[int] = None,
    great: Optional[int] = None,
    good: Optional[int] = None,
    bad: Optional[int] = None,
    miss: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SetTripleCastDaistarEnrollCount/{enrollCount}
@router.post(
    "/api/Debugs/SetTripleCastDaistarEnrollCount/{enrollCount}",
    name="Debug_SetTripleCastDaistarEnrollCount",
)
async def debug_set_triple_cast_daistar_enroll_count(
    request: Request, enrollCount: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debug/SetTripleCastGroupScore?tripleCastMasterId=&startScore=
@router.post("/api/Debug/SetTripleCastGroupScore", name="Debug_SetTripleCastGroupScore")
async def debug_set_triple_cast_group_score(
    request: Request,
    tripleCastMasterId: Optional[int] = None,
    startScore: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debug/SetTripleCastScore?tripleCastMasterId=&score=
@router.post("/api/Debug/SetTripleCastScore", name="Debug_SetTripleCastScore")
async def debug_set_triple_cast_score(
    request: Request,
    tripleCastMasterId: Optional[int] = None,
    score: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/SetUserBanLevel?banLevel=&bannedCount=
@router.post("/api/Debugs/SetUserBanLevel", name="Debug_SetUserBanLevel")
async def debug_set_user_ban_level(
    request: Request, banLevel: Optional[int] = None, bannedCount: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/UnlockAllFeatures
@router.post("/api/Debugs/UnlockAllFeatures", name="Debug_UnlockAllFeatures")
async def debug_unlock_all_features(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/LeagueUpdateRankingScore/{userId}/{leagueMasterId}/{leagueGroupId}/{score}
@router.post(
    "/api/Debugs/LeagueUpdateRankingScore/{userId}/{leagueMasterId}/{leagueGroupId}/{score}",
    name="Debug_UpdateRankingScore",
)
async def debug_update_ranking_score(
    request: Request, userId: int, leagueMasterId: int, leagueGroupId: int, score: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/UpdateUserProfileSnapshots?fromUserId=&toUserId=
@router.post(
    "/api/Debugs/UpdateUserProfileSnapshots", name="Debug_UpdateUserProfileSnapshots"
)
async def debug_update_user_profile_snapshots(
    request: Request, fromUserId: Optional[int] = None, toUserId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Debugs/UploadToutchLog
@router.post("/api/Debugs/UploadToutchLog", name="Debug_UploadToutchLog")
async def debug_upload_toutch_log(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request)
    return respond(UrlResult())
