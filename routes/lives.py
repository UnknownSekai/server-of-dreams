from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import read_request, respond
from helpers.stamina import adjust_and_check_stamina  # noqa: F401  (see Start routes)
from models import *

router = APIRouter(tags=["Lives"])


# /api/Lives/CalculateLessonTimingEvents
@router.post(
    "/api/Lives/CalculateLessonTimingEvents", name="Lives_CalculateLessonTimingEvents"
)
async def lives_calculate_lesson_timing_events(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, CalculateLessonTimeEventPayload)
    return respond(LiveTimeEvent())


# /api/Lives/CalculateTimingEvents
@router.post("/api/Lives/CalculateTimingEvents", name="Lives_CalculateTimeEvents")
async def lives_calculate_time_events(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, CalculateTimeEventPayload)
    return respond(LiveTimeEvent())


# /api/Lives/Music/EditBookmark
@router.post("/api/Lives/Music/EditBookmark", name="Lives_EditBookmark")
async def lives_edit_bookmark(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, EditBookmarkPayload)
    return respond(BooleanResult())


# /api/Lives/FinishAndValidate
@router.post("/api/Lives/FinishAndValidate", name="Lives_FinishAndValidate")
async def lives_finish_and_validate(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, FinishLivePayload)
    return respond(FinishLiveResult())


# /api/Lives/FinishAnotherNotationLive
@router.post(
    "/api/Lives/FinishAnotherNotationLive", name="Lives_FinishAnotherNotationLive"
)
async def lives_finish_another_notation_live(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, FinishAnotherNotationLivePayload)
    return respond(FinishLiveResult())


# /api/Lives/GetCourseCircleRanking/{mMusicCourseId}
@router.post(
    "/api/Lives/GetCourseCircleRanking/{mMusicCourseId}",
    name="Lives_GetCourseCircleRanking",
)
async def lives_get_course_circle_ranking(request: Request, mMusicCourseId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])


# /api/Lives/GetCourseFriendRanking/{mMusicCourseId}
@router.post(
    "/api/Lives/GetCourseFriendRanking/{mMusicCourseId}",
    name="Lives_GetCourseFriendRanking",
)
async def lives_get_course_friend_ranking(request: Request, mMusicCourseId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])


# /api/Lives/GetCourseNearRanking/{mMusicCourseId}
@router.post(
    "/api/Lives/GetCourseNearRanking/{mMusicCourseId}",
    name="Lives_GetCourseNearRanking",
)
async def lives_get_course_near_ranking(request: Request, mMusicCourseId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])


# /api/Lives/GetCourseTopRanking/{mMusicCourseId}
@router.post(
    "/api/Lives/GetCourseTopRanking/{mMusicCourseId}", name="Lives_GetCourseTopRanking"
)
async def lives_get_course_top_ranking(request: Request, mMusicCourseId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])


# /api/Lives/GetMultiLiveInformation/{multiLiveId}
@router.get(
    "/api/Lives/GetMultiLiveInformation/{multiLiveId}",
    name="Lives_GetMultiLiveInformation",
)
async def lives_get_multi_live_information(request: Request, multiLiveId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(MultiLiveInformation())


# /api/Lives/MatchingGhostLive
@router.post("/api/Lives/MatchingGhostLive", name="Lives_MatchingGhostLive")
async def lives_matching_ghost_live(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(MatchingGhostLiveResult())


# /api/Lives/ReadConcertTips?mConcertId=
@router.post("/api/Lives/ReadConcertTips", name="Lives_ReadConcertTips")
async def lives_read_concert_tips(request: Request, mConcertId: Optional[int] = None):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Lives/ReceiveTeamChallengeRewards?uMultiLiveId=
@router.post(
    "/api/Lives/ReceiveTeamChallengeRewards", name="Lives_ReceiveTeamChallengeRewards"
)
async def lives_receive_team_challenge_rewards(
    request: Request, uMultiLiveId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])


# /api/Lives/Retire
@router.post("/api/Lives/Retire", name="Lives_Retire")
async def lives_retire(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Lives/SelectMusicCourseRandomMusic
@router.post(
    "/api/Lives/SelectMusicCourseRandomMusic", name="Lives_SelectMusicCourseRandomMusic"
)
async def lives_select_music_course_random_music(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, SelectMusicCourseRandomMusicPayload)
    return respond(MusicCourseRandomSelectResult())


# /api/Lives/Start
@router.post("/api/Lives/Start", name="Lives_Start")
async def lives_start(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, StartLivePayload)
    # TODO consume stamina before the live (same for StartBonusLive / StartConcert):
    #   async with app.acquire_db() as conn:
    #       if not await adjust_and_check_stamina(conn, user_id, -cost, player_rank):
    #           return respond(BooleanResult(is_success=False))  # not enough stamina
    return respond(LiveUnit())


# /api/Lives/StartBonusLive
@router.post("/api/Lives/StartBonusLive", name="Lives_StartBonusLive")
async def lives_start_bonus_live(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, StartLivePayload)
    return respond(LiveUnit())


# /api/Lives/StartConcert
@router.post("/api/Lives/StartConcert", name="Lives_StartConcert")
async def lives_start_concert(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, StartLivePayload)
    return respond(LiveUnit())


# /api/Lives/StartGhostLive
@router.post("/api/Lives/StartGhostLive", name="Lives_StartGhostLive")
async def lives_start_ghost_live(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, StartLivePayload)
    return respond(LiveUnit())


# /api/Lives/StartLesson
@router.post("/api/Lives/StartLesson", name="Lives_StartLesson")
async def lives_start_lesson(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, StartLessonPayload)
    return respond(LiveUnit())


# /api/Lives/StartMultiLive
@router.post("/api/Lives/StartMultiLive", name="Lives_StartMultiLive")
async def lives_start_multi_live(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, StartMultiLivePayload)
    return respond(LiveUnit())


# /api/Lives/StartMultiRoomLive
@router.post("/api/Lives/StartMultiRoomLive", name="Lives_StartMultiRoomLive")
async def lives_start_multi_room_live(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, StartMultiRoomLivePayload)
    return respond(LiveUnit())


# /api/Lives/StartMusicCourseLive
@router.post("/api/Lives/StartMusicCourseLive", name="Lives_StartMusicCourse")
async def lives_start_music_course(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, StartLivePayload)
    return respond(LiveUnit())


# /api/Lives/StartTournament
@router.post("/api/Lives/StartTournament", name="Lives_StartTournament")
async def lives_start_tournament(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, StartTournamentPayload)
    return respond(LiveUnit())


# /api/Lives/StartTrialPartyEventStage
@router.post(
    "/api/Lives/StartTrialPartyEventStage", name="Lives_StartTrialPartyEventStage"
)
async def lives_start_trial_party_event_stage(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, StartLivePayload)
    return respond(LiveUnit())


# /api/Lives/StartTripleCastLive
@router.post("/api/Lives/StartTripleCastLive", name="Lives_StartTripleCastLive")
async def lives_start_triple_cast_live(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, StartTripleCastLivePayload)
    return respond(StartTripleCastLiveResult())


# /api/Lives/UpdateClearLamps/{multiLiveId}
@router.post("/api/Lives/UpdateClearLamps/{multiLiveId}", name="Lives_UpdateClearLamp")
async def lives_update_clear_lamp(request: Request, multiLiveId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(UpdateClearLampResult())
