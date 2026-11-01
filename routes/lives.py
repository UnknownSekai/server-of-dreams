from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from db.user import (
    create_active_live,
    delete_active_lives,
    get_active_live,
    get_lives,
    get_partys,
    get_sp_rates,
    get_users,
    next_live_id,
    update_live_result,
    update_player_rate,
    update_sp_rate_point,
    upsert_live,
    upsert_music_bookmark,
    upsert_sp_rate,
)
from helpers.cache import cache
from helpers.live import build_live_time_event, build_live_unit
from helpers.live_drops import grant_frames, resolve_frames
from helpers.live_rate import (
    chart_live_rate,
    chart_live_rate_result,
    olivier_sp_rate_points,
    total_of_live_rates,
)
from helpers.live_result import (
    achievement_rate,
    clear_lamp,
    good_or_worse_count,
    non_perfect_star_count,
    play_totals,
    rate_grade,
)
from helpers.music_unlock import affects_unlocks, apply_unlocks, stella_unlocked_by
from helpers.msgpack import fault, read_request, respond
from helpers.score import verify_score_blocks
from helpers.stamina import adjust_and_check_stamina
from helpers.things import present_type
from helpers.user_data import build_present, current_user_id, data_object
from models import *
from models.database import LiveModel, MusicBookmarkModel, SpRateModel

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
    user_id = current_user_id(request)
    payload = await read_request(request, EditBookmarkPayload)
    if user_id is None or payload is None or payload.music_master_id <= 0:
        return respond(BooleanResult())
    music_id = payload.music_master_id
    flag = int(payload.bookmark_flag)
    # the flag is a 3-bit mask (Bookmark1/2/4); the enum admits arbitrary ints, so reject
    # anything outside those bits and any unknown song.
    if flag < 0 or flag & ~7 or not any(m.id_ == music_id for m in cache.music_master):
        return respond(BooleanResult())
    async with app.acquire_db() as conn, conn.transaction():
        # music_bookmark has no unique (userId, musicMasterId) key, so serialize this
        # account/song pair to stop repeated taps leaving duplicate rows. Replace the row
        # outright: flag 0 just clears it.
        await conn.conn.execute(
            "SELECT pg_advisory_xact_lock(hashtextextended($1, 0))",
            f"music-bookmark:{user_id}:{music_id}",
        )
        existed = await conn.conn.fetchval(
            'SELECT 1 FROM "music_bookmark" WHERE "userId" = $1 AND "musicMasterId" = $2 LIMIT 1',
            user_id,
            music_id,
        )
        await conn.conn.execute(
            'DELETE FROM "music_bookmark" WHERE "userId" = $1 AND "musicMasterId" = $2',
            user_id,
            music_id,
        )
        if flag:
            await conn.execute(
                upsert_music_bookmark(
                    user_id, {"musicMasterId": music_id, "musicBookmarkFlag": flag}
                )
            )
    if not existed and not flag:  # nothing was there and nothing to set
        return respond(BooleanResult(is_success=True))
    return respond(
        BooleanResult(is_success=True),
        present=[
            data_object(
                "MusicBookmark",
                MusicBookmarkModel(
                    userId=user_id, musicMasterId=music_id, musicBookmarkFlag=flag
                ),
            )
        ],
    )


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
        # A finish records two separable things. The *score* -- achievement rate + grade -- is
        # kept on any manual play, a failed one (life hit 0) included; the game still shows it.
        # The *rating* -- the chart/player live rate, the clear lamp and SpRate -- is only earned
        # by a clear, so a fail shows "算出されません" for those. An auto-play run banks neither
        # (it would otherwise hand out a free 101% All Perfect); both still count as a play and
        # still drop rewards.
        auto_play = bool(active.isAutoPlay) if active is not None else False
        score_counts = not auto_play  # achievement rate + grade (kept even on a fail)
        rating_counts = is_cleared and not auto_play  # live rate, clear lamp, SpRate
        is_high_score = score_counts and this_rate > prev_rate

        best_lamp = max(before_lamp, new_lamp) if rating_counts else before_lamp
        best_rate = max(prev_rate, this_rate) if score_counts else prev_rate
        best_grade = rate_grade(best_rate)
        # the rate this run feeds into live-rate math: the real figure on a counted clear,
        # otherwise the prior best (so a fail / auto play moves no rating).
        effective_rate = this_rate if rating_counts else prev_rate
        times = (existing.timesCompleted if existing is not None else 0) + 1
        # the chart's live rate (the rating) only moves on a clear; a fail keeps the prior value
        notation_rate = (
            (chart_live_rate(live_master_id, best_rate) or 0.0)
            if rating_counts
            else (existing.notationRate if existing is not None else 0.0)
        )

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
        elif live_master_id and score_counts:
            # a manual play (clear or fail) mints the record so its achievement rate is kept;
            # an auto play banks nothing, so it leaves no row behind.
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

        # the updated owned Live row goes in present so the client's records reflect it (only
        # when a row was actually written -- an existing record, or a counted clear)
        present: list = []
        if live_master_id and (existing is not None or score_counts):
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
            # the Extra GOOD budget can only be judged here, off this play's own blocks
            changed = await apply_unlocks(
                conn,
                user_id,
                stella_unlocked_by(
                    live_master_id,
                    is_cleared,
                    good_or_worse_count(payload.base_score_blocks),
                ),
            )
            present += [data_object("Music", music) for music in changed]

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
        lr_best, lr_this = chart_live_rate_result(
            live_master_id, effective_rate, prev_rate
        )
        live_rate_result = RateUpdateResult(best_ever=lr_best, this_time=lr_this)
        # the player rate is the top-30 of the stored per-chart live rates (notationRate), which
        # only a clear moves -- so a fail keeps its contribution unchanged (rating not given).
        total_before = total_of_live_rates(r.notationRate for r in lives)
        after_notations = [
            r.notationRate for r in lives if r.liveMasterId != live_master_id
        ]
        if live_master_id and (existing is not None or score_counts):
            after_notations.append(notation_rate)
        total_after = total_of_live_rates(after_notations)
        if total_after != total_before:
            await conn.execute(update_player_rate(user_id, total_after))

        # Olivier (difficulty 5) clears award star-badge points (SpRate) instead of a live
        # rate: keep the chart's best points and report the before/after per-chart + total.
        sp_rate_update_result = None
        this_points = (
            olivier_sp_rate_points(
                live_master_id,
                this_rate,
                new_lamp,
                non_perfect_star_count(payload.base_score_blocks),
            )
            if rating_counts
            else None
        )
        if this_points is not None:
            sp_rows = await conn.fetch(get_sp_rates(user_id))
            existing_sp = next(
                (r for r in sp_rows if r.liveMasterId == live_master_id), None
            )
            before_best = existing_sp.point if existing_sp is not None else 0
            before_total = sum(r.point for r in sp_rows)
            new_best = max(before_best, this_points)
            after_total = before_total - before_best + new_best
            if existing_sp is not None:
                sp_id = existing_sp.id
                if new_best != before_best:
                    await conn.execute(update_sp_rate_point(user_id, sp_id, new_best))
            else:
                sp_id = max((r.id for r in sp_rows), default=0) + 1
                await conn.execute(
                    upsert_sp_rate(
                        user_id,
                        {
                            "id": sp_id,
                            "liveMasterId": live_master_id,
                            "point": new_best,
                        },
                    )
                )
            sp_rate_update_result = SpRateUpdateResult(
                best_ever=before_best,
                this_time=this_points,
                best_ever_total=before_total,
                this_time_total=after_total,
            )
            present.append(
                data_object(
                    "SpRate",
                    SpRateModel(
                        userId=user_id,
                        id=sp_id,
                        liveMasterId=live_master_id,
                        point=new_best,
                    ),
                )
            )

    # refresh what this finish changed for the client: drop rewards + the player rating
    refresh: set = set()
    if live_drops:
        refresh |= {present_type(int(d.received_thing.type)) for d in live_drops}
        refresh.discard(None)
    if total_after != total_before:
        refresh.add("UserProfile")
    if refresh:
        present += await build_present(app, user_id, *sorted(refresh))

    # the result panel mirrors the save: a manual run reports its own achievement rate + grade
    # (a fail included), an auto play reports the prior best (no fresh All Perfect), and only a
    # clear shows a clear lamp. The live rate / SpRate are untouched by a fail, so the client
    # renders "算出されません" for the rating while still showing the achievement rate.
    result_lamp = new_lamp if score_counts else before_lamp
    display_rate = this_rate if score_counts else prev_rate
    result = FinishLiveResult(
        clear_lamp=ClearLamps(result_lamp),
        before_clear_lamp=ClearLamps(before_lamp),
        rate_grade=AchievementRateGrades(rate_grade(display_rate)),
        is_high_score=is_high_score,
        achievement_rate_average=0.0,  # TODO: add global average acc
        rate_result=RateResult(
            achievement_rate_result=RateUpdateResult(
                best_ever=round(prev_rate, 4),
                this_time=round(display_rate, 4),  # best_ever = past best only
            ),
            live_rate_result=live_rate_result,
            total_rate_before=total_before,
            total_rate_after=total_after,
        ),
        sp_rate_update_result=sp_rate_update_result,
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
                    payload.is_auto_play,
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
    user_id = current_user_id(request)
    payload = await read_request(request, StartMultiLivePayload)
    present: list = []
    unit = LiveUnit()
    if user_id is not None and payload is not None:
        async with app.acquire_db() as conn:
            user = await conn.fetchrow(get_users(user_id))
            stamina_spent = False
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
                    user = await conn.fetchrow(get_users(user_id))

            party_id = payload.party_id
            if not party_id:
                parties = await conn.fetch(get_partys(user_id))
                party_id = parties[0].id if parties else 1

            # Determine the liveSettingMasterId from the active room if available,
            # falling back to the standard multi-live hall (11: Sirius)
            live_setting_master_id = 11
            rt = getattr(app, "realtime_service", None)
            if rt is not None and getattr(rt, "registry", None) is not None:
                room = rt.registry.room_by_user_id(user_id)
                if room is None and payload.multi_live_id:
                    room = rt.registry.room_by_multi_live_id(payload.multi_live_id)
                if room is not None and room.live_setting_master_id:
                    live_setting_master_id = room.live_setting_master_id

            await conn.execute(delete_active_lives(user_id))
            unit, live_id = await build_live_unit(
                conn, user_id, party_id, payload.live_master_id
            )
            await conn.execute(
                create_active_live(
                    user_id,
                    live_id,
                    payload.live_master_id,
                    party_id,
                    live_setting_master_id,
                    stamina_spent,
                )
            )
            present = (
                [data_object("User", user)]
                if user is not None and stamina_spent
                else []
            )
    return respond(unit, present=present)


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
