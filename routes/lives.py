from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/Lives", tags=["Lives"])


# /api/Lives/CalculateLessonTimingEvents
@router.post(
    "/CalculateLessonTimingEvents",
    response_model=LiveTimeEvent,
    name="Lives_CalculateLessonTimingEvents",
)
async def lives_calculate_lesson_timing_events(
    body: CalculateLessonTimeEventPayload,
) -> LiveTimeEvent:
    return LiveTimeEvent()


# /api/Lives/CalculateTimingEvents
@router.post(
    "/CalculateTimingEvents",
    response_model=LiveTimeEvent,
    name="Lives_CalculateTimeEvents",
)
async def lives_calculate_time_events(body: CalculateTimeEventPayload) -> LiveTimeEvent:
    return LiveTimeEvent()


# /api/Lives/FinishAndValidate
@router.post(
    "/FinishAndValidate",
    response_model=FinishLiveResult,
    name="Lives_FinishAndValidate",
)
async def lives_finish_and_validate(body: FinishLivePayload) -> FinishLiveResult:
    return FinishLiveResult()


# /api/Lives/FinishAnotherNotationLive
@router.post(
    "/FinishAnotherNotationLive",
    response_model=FinishLiveResult,
    name="Lives_FinishAnotherNotationLive",
)
async def lives_finish_another_notation_live(
    body: FinishAnotherNotationLivePayload,
) -> FinishLiveResult:
    return FinishLiveResult()


# /api/Lives/MatchingGhostLive
@router.post(
    "/MatchingGhostLive",
    response_model=MatchingGhostLiveResult,
    name="Lives_MatchingGhostLive",
)
async def lives_matching_ghost_live() -> MatchingGhostLiveResult:
    return MatchingGhostLiveResult()


# /api/Lives/Music/EditBookmark
@router.post(
    "/Music/EditBookmark", response_model=BooleanResult, name="Lives_EditBookmark"
)
async def lives_edit_bookmark(body: EditBookmarkPayload) -> BooleanResult:
    return BooleanResult()


# /api/Lives/Retire
@router.post("/Retire", response_model=BooleanResult, name="Lives_Retire")
async def lives_retire() -> BooleanResult:
    return BooleanResult()


# /api/Lives/SelectMusicCourseRandomMusic
@router.post(
    "/SelectMusicCourseRandomMusic",
    response_model=MusicCourseRandomSelectResult,
    name="Lives_SelectMusicCourseRandomMusic",
)
async def lives_select_music_course_random_music(
    body: SelectMusicCourseRandomMusicPayload,
) -> MusicCourseRandomSelectResult:
    return MusicCourseRandomSelectResult()


# /api/Lives/Start
@router.post("/Start", response_model=LiveUnit, name="Lives_Start")
async def lives_start(body: StartLivePayload) -> LiveUnit:
    return LiveUnit()


# /api/Lives/StartBonusLive
@router.post("/StartBonusLive", response_model=LiveUnit, name="Lives_StartBonusLive")
async def lives_start_bonus_live(body: StartLivePayload) -> LiveUnit:
    return LiveUnit()


# /api/Lives/StartConcert
@router.post("/StartConcert", response_model=LiveUnit, name="Lives_StartConcert")
async def lives_start_concert(body: StartLivePayload) -> LiveUnit:
    return LiveUnit()


# /api/Lives/StartGhostLive
@router.post("/StartGhostLive", response_model=LiveUnit, name="Lives_StartGhostLive")
async def lives_start_ghost_live(body: StartLivePayload) -> LiveUnit:
    return LiveUnit()


# /api/Lives/StartLesson
@router.post("/StartLesson", response_model=LiveUnit, name="Lives_StartLesson")
async def lives_start_lesson(body: StartLessonPayload) -> LiveUnit:
    return LiveUnit()


# /api/Lives/StartMultiLive
@router.post("/StartMultiLive", response_model=LiveUnit, name="Lives_StartMultiLive")
async def lives_start_multi_live(body: StartMultiLivePayload) -> LiveUnit:
    return LiveUnit()


# /api/Lives/StartMultiRoomLive
@router.post(
    "/StartMultiRoomLive", response_model=LiveUnit, name="Lives_StartMultiRoomLive"
)
async def lives_start_multi_room_live(body: StartMultiRoomLivePayload) -> LiveUnit:
    return LiveUnit()


# /api/Lives/StartMusicCourseLive
@router.post(
    "/StartMusicCourseLive", response_model=LiveUnit, name="Lives_StartMusicCourse"
)
async def lives_start_music_course(body: StartLivePayload) -> LiveUnit:
    return LiveUnit()


# /api/Lives/StartTournament
@router.post("/StartTournament", response_model=LiveUnit, name="Lives_StartTournament")
async def lives_start_tournament(body: StartTournamentPayload) -> LiveUnit:
    return LiveUnit()


# /api/Lives/StartTrialPartyEventStage
@router.post(
    "/StartTrialPartyEventStage",
    response_model=LiveUnit,
    name="Lives_StartTrialPartyEventStage",
)
async def lives_start_trial_party_event_stage(body: StartLivePayload) -> LiveUnit:
    return LiveUnit()


# /api/Lives/StartTripleCastLive
@router.post(
    "/StartTripleCastLive",
    response_model=StartTripleCastLiveResult,
    name="Lives_StartTripleCastLive",
)
async def lives_start_triple_cast_live(
    body: StartTripleCastLivePayload,
) -> StartTripleCastLiveResult:
    return StartTripleCastLiveResult()
