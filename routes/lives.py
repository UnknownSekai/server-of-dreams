import random
from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from db.user import create_active_live, delete_active_lives, get_users
from helpers.cache import cache
from helpers.live import build_live_time_event, build_live_unit
from helpers.msgpack import fault, read_request, respond
from helpers.score import verify_score_blocks
from helpers.stamina import adjust_and_check_stamina
from helpers.user_data import current_user_id, data_object
from models import *

router = APIRouter(tags=["Lives"])

_LIVE_MASTER: dict = {}
_MUSIC_MASTER: dict = {}


def _stamina_cost(live_master_id: int, ratio: int) -> int:
    # LiveMaster -> MusicMaster.stamina_consumption, scaled by the play's ratio
    if not _LIVE_MASTER:
        _LIVE_MASTER.update({m.id_: m for m in cache.live_master})
        _MUSIC_MASTER.update({m.id_: m for m in cache.music_master})
    live = _LIVE_MASTER.get(live_master_id)
    music = _MUSIC_MASTER.get(live.music_master_id) if live is not None else None
    base = music.stamina_consumption if music is not None else 0
    return base * max(1, int(ratio))


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
    user_id = current_user_id(request)
    payload = await read_request(request, CalculateTimeEventPayload)
    lte = LiveTimeEvent()
    if user_id is not None and payload is not None:
        async with app.acquire_db() as conn:
            lte = await build_live_time_event(
                conn,
                user_id,
                payload.party_id,
                payload.music_master_id,
                payload.sense_notation_master_id,  # None -> normal (duration-based)
            )
    return respond(lte)


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
    if payload is not None and not verify_score_blocks(payload):
        # score-block hash chain does not reproduce -> tampered score, reject
        return respond(FinishLiveResult(), faults=[fault("InvalidScoreBlockHash")])
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
    user_id = current_user_id(request)
    if user_id is not None:
        async with app.acquire_db() as conn:
            await conn.execute(delete_active_lives(user_id))
    return respond(BooleanResult(is_success=True))


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
    user_id = current_user_id(request)
    payload = await read_request(request, StartLivePayload)
    present: list = []
    unit = LiveUnit()
    if user_id is not None and payload is not None:
        async with app.acquire_db() as conn:
            user = await conn.fetchrow(get_users(user_id))
            if user is not None and payload.use_stamina:
                cost = _stamina_cost(
                    payload.live_master_id, payload.stamina_consumption_ratio
                )
                if cost > 0 and await adjust_and_check_stamina(
                    conn, user_id, -cost, user.playerRank
                ):
                    user = await conn.fetchrow(
                        get_users(user_id)
                    )  # reflect spent stamina
            await conn.execute(delete_active_lives(user_id))  # one active live per user
            unit, live_id = await build_live_unit(
                conn, user_id, payload.party_id, payload.live_master_id
            )
            await conn.execute(
                create_active_live(
                    user_id, live_id, payload.live_master_id, payload.party_id
                )
            )
            present = [data_object("User", user)] if user is not None else []
    return respond(unit, present=present)


# /api/Lives/StartBonusLive
@router.post("/api/Lives/StartBonusLive", name="Lives_StartBonusLive")
async def lives_start_bonus_live(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, StartLivePayload)
    # scripted: time_events = build_live_time_event(conn, user_id, party_id,
    #   music_master_id, bonus_live_stage_master.sense_notation_master_id)
    return respond(LiveUnit())


# /api/Lives/StartConcert
@router.post("/api/Lives/StartConcert", name="Lives_StartConcert")
async def lives_start_concert(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, StartLivePayload)
    # scripted: time_events = build_live_time_event(conn, user_id, party_id,
    #   music_master_id, concert_stage_master.sense_notation_master_id)
    return respond(LiveUnit())


# /api/Lives/StartGhostLive
@router.post("/api/Lives/StartGhostLive", name="Lives_StartGhostLive")
async def lives_start_ghost_live(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, StartLivePayload)
    # scripted: time_events = build_live_time_event(conn, user_id, party_id,
    #   music_master_id, ghost_live_master.sense_notation_master_id)
    return respond(LiveUnit())


# /api/Lives/StartLesson
@router.post("/api/Lives/StartLesson", name="Lives_StartLesson")
async def lives_start_lesson(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, StartLessonPayload)
    # scripted: time_events = build_live_time_event(conn, user_id, party_id,
    #   music_master_id, sense_notation_master_id)  # lesson sense-notation source TBD
    return respond(LiveUnit())


# /api/Lives/StartMultiLive
@router.post("/api/Lives/StartMultiLive", name="Lives_StartMultiLive")
async def lives_start_multi_live(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, StartMultiLivePayload)
    # scripted: time_events = build_live_time_event(conn, user_id, party_id,
    #   music_master_id, league_master.sense_notation_master_id)  # league/multi source TBD
    return respond(LiveUnit())


# /api/Lives/StartMultiRoomLive
@router.post("/api/Lives/StartMultiRoomLive", name="Lives_StartMultiRoomLive")
async def lives_start_multi_room_live(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, StartMultiRoomLivePayload)
    # scripted: time_events = build_live_time_event(conn, user_id, party_id,
    #   music_master_id, league_master.sense_notation_master_id)  # league/multi source TBD
    return respond(LiveUnit())


# /api/Lives/StartMusicCourseLive
@router.post("/api/Lives/StartMusicCourseLive", name="Lives_StartMusicCourse")
async def lives_start_music_course(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, StartLivePayload)
    # scripted: time_events = build_live_time_event(conn, user_id, party_id,
    #   music_master_id, sense_notation_master_id)  # music-course sense-notation source TBD
    return respond(LiveUnit())


# /api/Lives/StartTournament
@router.post("/api/Lives/StartTournament", name="Lives_StartTournament")
async def lives_start_tournament(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, StartTournamentPayload)
    # scripted: time_events = build_live_time_event(conn, user_id, party_id,
    #   music_master_id, league_master.sense_notation_master_id)  # tournament source TBD
    return respond(LiveUnit())


# /api/Lives/StartTrialPartyEventStage
@router.post(
    "/api/Lives/StartTrialPartyEventStage", name="Lives_StartTrialPartyEventStage"
)
async def lives_start_trial_party_event_stage(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, StartLivePayload)
    # scripted: time_events = build_live_time_event(conn, user_id, party_id,
    #   music_master_id, trial_party_event_stage_master.sense_notation_master_id)
    return respond(LiveUnit())


# /api/Lives/StartTripleCastLive
@router.post("/api/Lives/StartTripleCastLive", name="Lives_StartTripleCastLive")
async def lives_start_triple_cast_live(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, StartTripleCastLivePayload)
    # scripted: one build_live_time_event per unit, from
    #   triple_cast_master.sense_notation_master_id{1,2,3}
    return respond(StartTripleCastLiveResult())


# /api/Lives/UpdateClearLamps/{multiLiveId}
@router.post("/api/Lives/UpdateClearLamps/{multiLiveId}", name="Lives_UpdateClearLamp")
async def lives_update_clear_lamp(request: Request, multiLiveId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(UpdateClearLampResult())
