from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from db.user import (
    create_active_live,
    delete_active_lives,
    get_active_live,
    get_lives,
    get_musics,
    get_users,
    next_live_id,
    update_live_result,
    update_music_releases,
    update_player_rate,
    upsert_live,
)
from helpers.cache import cache
from helpers.live import build_live_time_event, build_live_unit
from helpers.live_drops import grant_frames, resolve_frames
from helpers.live_rate import chart_live_rate, chart_live_rate_result, total_rate
from helpers.live_result import achievement_rate, clear_lamp, play_totals, rate_grade
from helpers.music_unlock import affects_unlocks, load_progress
from helpers.msgpack import fault, read_request, respond
from helpers.score import verify_score_blocks
from helpers.stamina import adjust_and_check_stamina
from helpers.things import present_type
from helpers.user_data import build_present, current_user_id, data_object
from models import *
from models.database import LiveModel

router = APIRouter(tags=["Lives"])

_LIVE_MASTER: dict = {}
_MUSIC_MASTER: dict = {}


def _music_of(live_master_id: int):
    # LiveMaster -> its MusicMaster
    if not _LIVE_MASTER:
        _LIVE_MASTER.update({m.id_: m for m in cache.live_master})
        _MUSIC_MASTER.update({m.id_: m for m in cache.music_master})
    live = _LIVE_MASTER.get(live_master_id)
    return _MUSIC_MASTER.get(live.music_master_id) if live is not None else None


def _is_long_version(live_master_id: int) -> bool:
    music = _music_of(live_master_id)
    return music.is_long_version if music is not None else False


def _stamina_cost(live_master_id: int, ratio: int) -> int:
    # MusicMaster.stamina_consumption, scaled by the play's ratio
    music = _music_of(live_master_id)
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
    user_id = current_user_id(request)
    payload = await read_request(request, FinishLivePayload)
    if payload is None:
        return respond(FinishLiveResult())
    if not verify_score_blocks(payload):
        # score-block hash chain does not reproduce -> tampered score, reject
        return respond(FinishLiveResult(), faults=[fault("InvalidScoreBlockHash")])
    if user_id is None:
        return respond(FinishLiveResult())

    # the client reports score=0 / max_combo=0 / is_cleared=false / judges=null and leaves the
    # rest to us, so lamp + rate + score all come out of the (hash-verified) score blocks
    score, is_cleared = play_totals(payload)
    new_lamp = clear_lamp(is_cleared, payload.base_score_blocks)
    this_rate = achievement_rate(payload.base_score_blocks)

    async with app.acquire_db() as conn:
        user = await conn.fetchrow(get_users(user_id))
        active = await conn.fetchrow(get_active_live(user_id))
        live_master_id = active.liveMasterId if active is not None else 0
        lives = await conn.fetch(get_lives(user_id)) if live_master_id else []
        existing = next((r for r in lives if r.liveMasterId == live_master_id), None)

        before_lamp = (
            existing.clearLamp if existing is not None else int(ClearLamps.None_)
        )
        prev_rate = existing.achievementRate if existing is not None else 0.0
        is_high_score = this_rate > prev_rate

        best_lamp = max(before_lamp, new_lamp)  # ClearLamps int order = worst..best
        best_rate = max(prev_rate, this_rate)
        best_grade = rate_grade(best_rate)
        times = (existing.timesCompleted if existing is not None else 0) + 1
        # notation_rate is the chart's (best) live rate: level + interpolated achievement bonus
        notation_rate = chart_live_rate(live_master_id, best_rate) or 0.0

        # the owned Live row's fields that this finish doesn't change carry over (or default)
        live_id = existing.id if existing is not None else 0
        live_status = (
            existing.status if existing is not None else int(LiveReleaseStatus.None_)
        )
        if existing is not None:
            await conn.execute(
                update_live_result(
                    user_id,
                    live_master_id,
                    times,
                    best_rate,
                    notation_rate,
                    best_lamp,
                    best_grade,
                )
            )
        elif live_master_id:
            id_row = await conn.fetchrow(next_live_id())
            live_id = id_row.value if id_row is not None else live_master_id
            await conn.execute(
                upsert_live(
                    user_id,
                    {
                        "id": live_id,
                        "liveMasterId": live_master_id,
                        "timesCompleted": times,
                        "achievementRate": best_rate,
                        "notationRate": notation_rate,
                        "clearLamp": best_lamp,
                        "status": live_status,
                        "rateGrade": best_grade,
                    },
                )
            )

        await conn.execute(delete_active_lives(user_id))  # consume the session

        # the updated owned Live row goes in present so the client's records reflect it
        present: list = []
        if live_master_id:
            present.append(
                data_object(
                    "Live",
                    LiveModel(
                        userId=user_id,
                        id=live_id,
                        liveMasterId=live_master_id,
                        timesCompleted=times,
                        achievementRate=best_rate,
                        notationRate=notation_rate,
                        clearLamp=best_lamp,
                        status=live_status,
                        rateGrade=best_grade,
                    ),
                )
            )

        # Only Extra/Stella/Olivier clears can change release state -- skip everything else.
        # When they can, re-derive every owned song, then push all changes in one UPDATE.
        if affects_unlocks(live_master_id):
            progress = await load_progress(conn, user_id)
            changes: list[tuple[int, bool, int]] = []
            for music in await conn.fetch(get_musics(user_id)):
                new_stella = progress.stella_released(
                    music.musicMasterId, music.isPossession, music.stellaReleased
                )
                new_status = progress.olivier_status(
                    music.musicMasterId, music.olivierReleaseStatus
                )
                if (
                    new_stella != music.stellaReleased
                    or new_status != music.olivierReleaseStatus
                ):
                    music.stellaReleased = new_stella
                    music.olivierReleaseStatus = new_status
                    changes.append((music.id, new_stella, new_status))
                    present.append(data_object("Music", music))
            if changes:
                await conn.execute(update_music_releases(user_id, changes))

        # live drops: resolve the setting's drop frames whose lot condition this play met,
        # then consolidate + batch-grant their rewards. Long-version songs never drop.
        live_drops: list[LiveDropThing] = []
        if not _is_long_version(live_master_id):
            setting_id = active.liveSettingMasterId if active is not None else 0
            frames = resolve_frames(
                setting_id,
                stamina_consumed=active.staminaSpent if active is not None else False,
                score=score,
                star_act_count=len(payload.star_act_score_blocks or []),
                achievement_rate=this_rate,
            )
            live_drops = await grant_frames(conn, user_id, frames)

        # live rate: this chart's (past-best, this-time) + the top-30 total before/after this
        # play. The profile's playerRate IS that top-30 total, so keep it in sync when it moves.
        # (0.0, 0.0) for charts with no live rate (Olivier / long-version) -- not null
        lr_best, lr_this = chart_live_rate_result(live_master_id, this_rate, prev_rate)
        live_rate_result = RateUpdateResult(best_ever=lr_best, this_time=lr_this)
        total_before = total_rate((r.liveMasterId, r.achievementRate) for r in lives)
        after_pairs = [
            (r.liveMasterId, r.achievementRate)
            for r in lives
            if r.liveMasterId != live_master_id
        ]
        if live_master_id:
            after_pairs.append((live_master_id, best_rate))
        total_after = total_rate(after_pairs)
        if total_after != total_before:
            await conn.execute(update_player_rate(user_id, total_after))

    # refresh what this finish changed for the client: drop rewards + the player rating
    refresh: set = set()
    if live_drops:
        refresh |= {present_type(int(d.received_thing.type)) for d in live_drops}
        refresh.discard(None)
    if total_after != total_before:
        refresh.add("UserProfile")
    if refresh:
        present += await build_present(app, user_id, *sorted(refresh))

    result = FinishLiveResult(
        clear_lamp=ClearLamps(new_lamp),
        before_clear_lamp=ClearLamps(before_lamp),
        rate_grade=AchievementRateGrades(best_grade),
        is_high_score=is_high_score,
        achievement_rate_average=0.0, # TODO: add global average acc
        rate_result=RateResult(
            achievement_rate_result=RateUpdateResult(
                best_ever=prev_rate, this_time=this_rate  # best_ever = past best only
            ),
            live_rate_result=live_rate_result,
            total_rate_before=total_before,
            total_rate_after=total_after,
        ),
        # TODO: calculate player rank pts
        player_rank_point_result=PlayerRankPointResult(
            rank_before=user.playerRank,
            rank_after=user.playerRank,
            rank_point_before=user.currentRankPoint,
            rank_point_after=user.currentRankPoint,
            rank_point_acquired=0,
            stamina_before=user.currentStamina,
        ),
        live_drop_things=live_drops,
        # These must be empty lists, not null -- the result panel iterates them and a null
        # list NREs the client. Empty for now; TODO implement each:
        league_rewards=[],  # TODO: league-mode finish rewards
        audition_rewards=[],  # TODO: audition finish rewards
        story_event_rewards=[],  # TODO: story-event finish rewards
        accessory_auto_sell_convert_things=[],  # TODO: accessories auto-sold to items on drop
    )
    return respond(result, present=present)


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
            stamina_spent = False
            # long-version songs never consume stamina
            if (
                user is not None
                and payload.use_stamina
                and not _is_long_version(payload.live_master_id)
            ):
                cost = _stamina_cost(
                    payload.live_master_id, payload.stamina_consumption_ratio
                )
                if cost > 0 and await adjust_and_check_stamina(
                    conn, user_id, -cost, user.playerRank
                ):
                    stamina_spent = True
                    user = await conn.fetchrow(
                        get_users(user_id)
                    )  # reflect spent stamina
            await conn.execute(delete_active_lives(user_id))  # one active live per user
            unit, live_id = await build_live_unit(
                conn, user_id, payload.party_id, payload.live_master_id
            )
            await conn.execute(
                create_active_live(
                    user_id,
                    live_id,
                    payload.live_master_id,
                    payload.party_id,
                    payload.live_setting_master_id,
                    stamina_spent,
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
