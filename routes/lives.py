from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/Lives", tags=["Lives"])


# /api/Lives/CalculateLessonTimingEvents
@router.post("/CalculateLessonTimingEvents", name="Lives_CalculateLessonTimingEvents")
async def lives_calculate_lesson_timing_events(request: Request):
    payload = await read_request(request, "CalculateLessonTimeEventPayload")
    return respond(LiveTimeEvent())


# /api/Lives/CalculateTimingEvents
@router.post("/CalculateTimingEvents", name="Lives_CalculateTimeEvents")
async def lives_calculate_time_events(request: Request):
    payload = await read_request(request, "CalculateTimeEventPayload")
    return respond(LiveTimeEvent())


# /api/Lives/FinishAndValidate
@router.post("/FinishAndValidate", name="Lives_FinishAndValidate")
async def lives_finish_and_validate(request: Request):
    payload = await read_request(request, "FinishLivePayload")
    return respond(FinishLiveResult())


# /api/Lives/FinishAnotherNotationLive
@router.post("/FinishAnotherNotationLive", name="Lives_FinishAnotherNotationLive")
async def lives_finish_another_notation_live(request: Request):
    payload = await read_request(request, "FinishAnotherNotationLivePayload")
    return respond(FinishLiveResult())


# /api/Lives/MatchingGhostLive
@router.post("/MatchingGhostLive", name="Lives_MatchingGhostLive")
async def lives_matching_ghost_live(request: Request):
    return respond(MatchingGhostLiveResult())


# /api/Lives/Music/EditBookmark
@router.post("/Music/EditBookmark", name="Lives_EditBookmark")
async def lives_edit_bookmark(request: Request):
    payload = await read_request(request, "EditBookmarkPayload")
    return respond(BooleanResult())


# /api/Lives/Retire
@router.post("/Retire", name="Lives_Retire")
async def lives_retire(request: Request):
    return respond(BooleanResult())


# /api/Lives/SelectMusicCourseRandomMusic
@router.post("/SelectMusicCourseRandomMusic", name="Lives_SelectMusicCourseRandomMusic")
async def lives_select_music_course_random_music(request: Request):
    payload = await read_request(request, "SelectMusicCourseRandomMusicPayload")
    return respond(MusicCourseRandomSelectResult())


# /api/Lives/Start
@router.post("/Start", name="Lives_Start")
async def lives_start(request: Request):
    payload = await read_request(request, "StartLivePayload")
    return respond(LiveUnit())


# /api/Lives/StartBonusLive
@router.post("/StartBonusLive", name="Lives_StartBonusLive")
async def lives_start_bonus_live(request: Request):
    payload = await read_request(request, "StartLivePayload")
    return respond(LiveUnit())


# /api/Lives/StartConcert
@router.post("/StartConcert", name="Lives_StartConcert")
async def lives_start_concert(request: Request):
    payload = await read_request(request, "StartLivePayload")
    return respond(LiveUnit())


# /api/Lives/StartGhostLive
@router.post("/StartGhostLive", name="Lives_StartGhostLive")
async def lives_start_ghost_live(request: Request):
    payload = await read_request(request, "StartLivePayload")
    return respond(LiveUnit())


# /api/Lives/StartLesson
@router.post("/StartLesson", name="Lives_StartLesson")
async def lives_start_lesson(request: Request):
    payload = await read_request(request, "StartLessonPayload")
    return respond(LiveUnit())


# /api/Lives/StartMultiLive
@router.post("/StartMultiLive", name="Lives_StartMultiLive")
async def lives_start_multi_live(request: Request):
    payload = await read_request(request, "StartMultiLivePayload")
    return respond(LiveUnit())


# /api/Lives/StartMultiRoomLive
@router.post("/StartMultiRoomLive", name="Lives_StartMultiRoomLive")
async def lives_start_multi_room_live(request: Request):
    payload = await read_request(request, "StartMultiRoomLivePayload")
    return respond(LiveUnit())


# /api/Lives/StartMusicCourseLive
@router.post("/StartMusicCourseLive", name="Lives_StartMusicCourse")
async def lives_start_music_course(request: Request):
    payload = await read_request(request, "StartLivePayload")
    return respond(LiveUnit())


# /api/Lives/StartTournament
@router.post("/StartTournament", name="Lives_StartTournament")
async def lives_start_tournament(request: Request):
    payload = await read_request(request, "StartTournamentPayload")
    return respond(LiveUnit())


# /api/Lives/StartTrialPartyEventStage
@router.post("/StartTrialPartyEventStage", name="Lives_StartTrialPartyEventStage")
async def lives_start_trial_party_event_stage(request: Request):
    payload = await read_request(request, "StartLivePayload")
    return respond(LiveUnit())


# /api/Lives/StartTripleCastLive
@router.post("/StartTripleCastLive", name="Lives_StartTripleCastLive")
async def lives_start_triple_cast_live(request: Request):
    payload = await read_request(request, "StartTripleCastLivePayload")
    return respond(StartTripleCastLiveResult())
