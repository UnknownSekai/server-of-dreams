"""Master-driven Anthology/audition progression + lesson & music-course lives.

These wrap the ``routes.lives`` Start/Finish/Retire handlers (via a per-request bound app
that shares the active transaction) and layer progression on top, so the base live logic
stays untouched. Installed by prepending the router, so these take precedence over the base
handlers.
"""

from contextlib import asynccontextmanager

from fastapi import APIRouter, Request

from db.user import create_active_live, delete_active_lives
from helpers.cache import cache
from helpers.game_state import Rejected, master, transaction
from helpers.live import build_live_time_event, build_live_unit
from helpers.live_result import play_totals
from helpers.msgpack import fault, from_array, read_request, respond
from helpers.progression import (
    context,
    daily,
    find_course,
    finish_context,
    lesson_party,
    lesson_slots,
    rules,
    stored_slots,
    use_daily,
)
from helpers.score import verify_score_blocks
from models import (
    BooleanResult,
    ConcertResult,
    FinishLivePayload,
    LiveUnit,
    SetLessonPartyPayload,
    StartLessonPayload,
    StartLivePayload,
    StartMultiLivePayload,
)
from routes import lives as upstream
from scripts._sirius import _decompress, _unpack_all

router = APIRouter(tags=["Lives"])


class BoundApp:
    def __init__(self, app, conn):
        self.app, self.conn = app, conn

    def __getattr__(self, name):
        return getattr(self.app, name)

    @asynccontextmanager
    async def acquire_db(self):
        yield self.conn


async def call_bound(request, s, fn):
    """Run an upstream handler inside this transaction by swapping in a bound app."""
    original = request.scope["app"]
    request.scope["app"] = BoundApp(original, s.conn)
    try:
        return await fn(request)
    finally:
        request.scope["app"] = original


def parts(response):
    return [_decompress(v) for v in _unpack_all(response.body)]


def concert_available(stage, cleared):
    siblings = sorted(
        m.id_
        for m in cache.concert_stage_master
        if m.concert_master_id == stage.concert_master_id
    )
    pos = siblings.index(stage.id_)
    return stage.id_ in cleared or pos == 0 or siblings[pos - 1] in cleared


def phases(ident):
    return sorted(
        (p for p in cache.audition_phase_master if p.auditionaster_id == ident),
        key=lambda p: p.phase,
    )


def attained(ident, score, acts, cleared):
    return max(
        [
            p.phase
            for p in phases(ident)
            if cleared and score >= p.clear_score and acts >= (p.star_act_count or 0)
        ]
        + [0]
    )


def rewards(rows):
    return [(int(r.thing_type), r.thing_id, r.thing_quantity) for r in rows or []]


@router.post("/api/Lives/Start")
@router.post("/api/Lives/StartConcert")
async def start(request: Request):
    try:
        p = await read_request(request, StartLivePayload)
        if p is None:
            raise Rejected("Missing payload")
        concert = request.url.path.endswith("StartConcert")
        mode, ident = (
            ("concert", p.concert_stage_master_id)
            if concert
            else ("audition", p.audition_master_id)
        )
        m = (
            master("concert_stage_master" if concert else "audition_master", ident)
            if ident
            else None
        )
        chart = master("live_master", p.live_master_id)
        if (
            not chart
            or (concert and not m)
            or (ident and not m)
            or (m and chart.music_master_id != m.music_master_id)
        ):
            raise Rejected("Invalid stage or chart")
        async with transaction(request) as s:
            if not await s.one("Party", id=p.party_id):
                raise Rejected("Missing party")
            if concert and not concert_available(
                m, {r["concertStageMasterId"] for r in await s.rows("ConcertStage")}
            ):
                raise Rejected("Stage is locked")
            await daily(s)
            r = parts(await call_bound(request, s, upstream.lives_start))
            active = await s.conn.conn.fetchrow(
                'SELECT * FROM active_live WHERE "userId"=$1', s.uid
            )
            music = master("music_master", chart.music_master_id)
            xp = (
                int(
                    music.stamina_consumption
                    * max(1, p.stamina_consumption_ratio)
                    * rules()["rank_xp_per_stamina"]
                )
                if active and active["staminaSpent"]
                else 0
            )
            await context(
                s,
                mode if m else "normal",
                ident or 0,
                {"rank_xp": xp, "auto": p.is_auto_play},
            )
            await s.conn.conn.execute(
                'DELETE FROM preservation_course_run WHERE "userId"=$1', s.uid
            )
            if m:
                unit = from_array("LiveUnit", r[1])
                lte = await build_live_time_event(
                    s.conn,
                    s.uid,
                    p.party_id,
                    m.music_master_id,
                    m.sense_notation_master_id,
                )
                unit.time_events = {t.timing_seconds: t.event for t in lte.timings}
                r[1] = unit
        return respond(r[1], faults=r[0], present=r[2] + s.present())
    except Rejected as e:
        return respond(None, faults=[fault("InvalidLiveStage", str(e))])


async def apply_progress(s, mode, ident, score, acts, cleared, result):
    m = master(
        "concert_stage_master" if mode == "concert" else "audition_master", ident
    )
    if not m:
        raise Rejected("Missing stage master")
    if mode == "concert":
        received = []
        if (
            cleared
            and score >= m.clear_score
            and not await s.one("ConcertStage", concertStageMasterId=ident)
        ):
            received = await s.grant(rewards(m.rewards))
            await s.insert("ConcertStage", concertStageMasterId=ident)
        result.concert_result = ConcertResult(rewards=received)
        return
    row = await s.one("AuditionClear", auditionMasterId=ident)
    before = max(row["clearPhase"], row["skipClearPhase"]) if row else 0
    achieved = min(before + 1, attained(ident, score, acts, cleared))
    result.audition_master_id = ident
    result.audition_before_phase = before
    result.audition_after_phase = max(before, achieved)
    things = []
    # the official challenge clear awards the stages in their master order
    targets = sorted(
        (
            x
            for x in cache.audition_master
            if x.audition_group_number == m.audition_group_number and x.id_ <= ident
        ),
        key=lambda x: x.id_,
    )
    for target in targets:
        target_phases = phases(target.id_)
        new = min(achieved, max([p.phase for p in target_phases] + [0]))
        if not new:
            continue
        existing = await s.one("AuditionClear", auditionMasterId=target.id_)
        old = max(existing["clearPhase"], existing["skipClearPhase"]) if existing else 0
        if new <= old:
            continue
        for phase in target_phases:
            if old < phase.phase <= new:
                package = master(
                    "audition_reward_package_master",
                    phase.audition_reward_package_master_id,
                )
                if not package:
                    raise Rejected("Missing reward package")
                things.extend(rewards(package.rewards))
        field = "clearPhase" if target.id_ == ident else "skipClearPhase"
        if existing:
            if new > existing[field]:
                await s.update("AuditionClear", existing, **{field: new})
        else:
            values = dict(
                auditionMasterId=target.id_,
                clearPhase=0,
                skipClearPhase=0,
                auditionClearPartyId=0,
            )
            values[field] = new
            await s.insert("AuditionClear", **values)
    # preserve reward entries in official order (including repeated item types)
    result.audition_rewards = []
    for thing in sorted(things, key=lambda t: t[0]):
        result.audition_rewards.extend(await s.grant([thing]))


@router.post("/api/Lives/StartMultiLive")
async def start_multi_live(request: Request):
    try:
        p = await read_request(request, StartMultiLivePayload)
        if p is None:
            raise Rejected("Missing payload")
        chart = master("live_master", p.live_master_id)
        if not chart:
            raise Rejected("Invalid live master")
        async with transaction(request) as s:
            r = parts(await call_bound(request, s, upstream.lives_start_multi_live))
            active = await s.conn.conn.fetchrow(
                'SELECT * FROM active_live WHERE "userId"=$1', s.uid
            )
            music = master("music_master", chart.music_master_id)
            xp = (
                int(
                    music.stamina_consumption
                    * max(1, p.stamina_consumption_ratio)
                    * rules()["rank_xp_per_stamina"]
                )
                if active and active["staminaSpent"] and music is not None
                else 0
            )
            await context(s, "normal", 0, {"rank_xp": xp})
        return respond(r[1], faults=r[0], present=r[2] + s.present())
    except Rejected as e:
        return respond(None, faults=[fault("InvalidLiveState", str(e))])


@router.post("/api/Lives/FinishAndValidate")
async def finish(request: Request):
    try:
        p = await read_request(request, FinishLivePayload)
        if p is None or not verify_score_blocks(p):
            raise Rejected("Invalid score blocks")
        async with transaction(request) as s:
            active = await s.conn.conn.fetchrow(
                'SELECT * FROM active_live WHERE "userId"=$1', s.uid
            )
            if not active:
                raise Rejected("No active live")
            context_row = await s.conn.conn.fetchrow(
                'SELECT * FROM preservation_live_context WHERE "userId"=$1', s.uid
            )
            r = parts(await call_bound(request, s, upstream.lives_finish_and_validate))
            if r[0]:
                raise Rejected("Live validation failed")
            result = from_array("FinishLiveResult", r[1])
            if context_row:
                score, cleared = play_totals(p)
                if context_row["mode"] in ("concert", "audition"):
                    await apply_progress(
                        s,
                        context_row["mode"],
                        context_row["masterId"],
                        score,
                        len(p.star_act_score_blocks or []),
                        cleared,
                        result,
                    )
                await finish_context(s, context_row, p, result)
            await s.conn.conn.execute(
                'DELETE FROM preservation_live_context WHERE "userId"=$1', s.uid
            )
            changed = s.present()
            keys = {(v[0], v[1][0]) for v in changed}
            present = [v for v in r[2] if (v[0], v[1][0]) not in keys] + changed
        return respond(result, present=present)
    except Rejected as e:
        from models import FinishLiveResult

        return respond(FinishLiveResult(), faults=[fault("InvalidLiveState", str(e))])


@router.post("/api/Lives/Retire")
async def retire(request: Request):
    async with transaction(request) as s:
        await s.conn.conn.execute(
            'DELETE FROM preservation_live_context WHERE "userId"=$1', s.uid
        )
        await s.conn.conn.execute(
            'DELETE FROM preservation_course_run WHERE "userId"=$1', s.uid
        )
        return await call_bound(request, s, upstream.lives_retire)


# ---- Lessons ----


@router.post("/api/Lessons/{base}/CreateParty")
async def create_lesson(request: Request, base: int):
    try:
        async with transaction(request) as s:
            await lesson_party(s, base)
        return respond(BooleanResult(is_success=True), present=s.present())
    except Rejected:
        return respond(BooleanResult())


@router.post("/api/Lessons/{base}/SetParty")
async def set_lesson(request: Request, base: int):
    try:
        p = await read_request(request, SetLessonPartyPayload)
        if not p or not p.slots:
            raise Rejected()
        async with transaction(request) as s:
            row = await lesson_party(s, base)
            slots, seen, positions = [], set(), set()
            for x in p.slots:
                if not 1 <= x.order <= 5 or x.order in positions:
                    raise Rejected()
                positions.add(x.order)
                if x.character_id:
                    c = await s.one("Character", id=x.character_id)
                    if (
                        not c
                        or x.character_id in seen
                        or master(
                            "character_master", c["characterMasterId"]
                        ).character_base_master_id
                        != base
                    ):
                        raise Rejected()
                    seen.add(x.character_id)
                slots.append([x.order, x.character_id or None])
            if not seen:
                raise Rejected()
            slots.extend([i, None] for i in range(1, 6) if i not in positions)
            leader = row["leaderPosition"]
            if leader and not any(i == leader and cid for i, cid in slots):
                leader = 0
            await s.update(
                "CharacterLesson",
                row,
                setCharacters=stored_slots(slots),
                leaderPosition=leader,
            )
        return respond(BooleanResult(is_success=True), present=s.present())
    except Rejected:
        return respond(BooleanResult())


@router.post("/api/Lessons/{base}/SetPartyLeader/{position}")
async def set_leader(request: Request, base: int, position: int):
    try:
        async with transaction(request) as s:
            row = await lesson_party(s, base)
            if not 0 <= position <= 5:
                raise Rejected()
            if position and not any(
                i == position and ident for i, ident in lesson_slots(row)
            ):
                raise Rejected()
            await s.update("CharacterLesson", row, leaderPosition=position)
        return respond(BooleanResult(is_success=True), present=s.present())
    except Rejected:
        return respond(BooleanResult())


@router.post("/api/Lives/StartLesson")
async def start_lesson(request: Request):
    from db import user as q

    try:
        p = await read_request(request, StartLessonPayload)
        if p is None:
            raise Rejected()
        base, chart = p.character_base_master_id, p.live_master_id
        if not master("live_master", chart):
            raise Rejected("Unknown chart")
        async with transaction(request) as s:
            row = await lesson_party(s, base)
            await daily(s)
            if not any(cid for _, cid in lesson_slots(row)):
                raise Rejected("Empty lesson party")
            # a temporary party exists only within this transaction and is removed before
            # return, so no phantom party or slot ever appears on the account
            party_id = max([r["id"] for r in await s.rows("Party")] + [0]) + 1
            await s.conn.execute(
                q.upsert_party(
                    s.uid,
                    dict(
                        id=party_id,
                        order=0,
                        name="Lesson",
                        leaderPosition=row["leaderPosition"] or 1,
                    ),
                )
            )
            sid = max([r["id"] for r in await s.rows("PartySlot")] + [0]) + 1
            for position, ident in lesson_slots(row):
                if not ident:
                    continue
                actor = await s.one("Character", id=ident)
                if (
                    not actor
                    or master(
                        "character_master", actor["characterMasterId"]
                    ).character_base_master_id
                    != base
                ):
                    raise Rejected("Invalid lesson actor")
                await s.conn.execute(
                    q.upsert_party_slot(
                        s.uid,
                        dict(
                            id=sid,
                            partyId=party_id,
                            position=position,
                            characterId=ident,
                            posterId=None,
                            accessoryId=None,
                            bonusAbilityEnableFlags=0,
                        ),
                    )
                )
                sid += 1
            unit, live_id = await build_live_unit(s.conn, s.uid, party_id, chart)
            await s.conn.conn.execute(
                'DELETE FROM party_slot WHERE "userId"=$1 AND "partyId"=$2',
                s.uid,
                party_id,
            )
            await s.conn.conn.execute(
                'DELETE FROM party WHERE "userId"=$1 AND id=$2', s.uid, party_id
            )
            await s.conn.execute(delete_active_lives(s.uid))
            await s.conn.execute(create_active_live(s.uid, live_id, chart, 0, 1, False))
            await s.conn.conn.execute(
                'DELETE FROM preservation_course_run WHERE "userId"=$1', s.uid
            )
            await context(s, "lesson", base, {"rank_xp": rules()["lesson_rank_xp"]})
        return respond(unit, present=s.present())
    except Rejected as e:
        return respond(None, faults=[fault("InvalidLesson", str(e))])


# ---- Music course ----


@router.post("/api/Lives/StartMusicCourseLive")
async def start_course(request: Request):
    import random
    import time

    try:
        p = await read_request(request, StartLivePayload)
        if p is None:
            raise Rejected()
        course, details, index = find_course(p.music_course_detail_master_id)
        d = details[index]
        if d.live_master_id != p.live_master_id or int(
            p.music_course_gauge_type
        ) not in (
            0,
            1,
        ):
            raise Rejected("Unsupported course chart")
        async with transaction(request) as s:
            old = await s.conn.conn.fetchrow(
                'SELECT * FROM preservation_course_run WHERE "userId"=$1', s.uid
            )
            active = await s.conn.conn.fetchrow(
                'SELECT * FROM preservation_live_context WHERE "userId"=$1', s.uid
            )
            if active and active["mode"] == "course":
                raise Rejected("Finish or retire the active stage first")
            if index == 0:
                usage = await daily(s)
                policy = rules()
                paid = "unlimited"
                if not policy["unlimited_attempts"]:
                    if (
                        usage["musicCourseFreeChallengeTimes"]
                        < policy["course_free_attempts"]
                    ):
                        await use_daily(s, "musicCourseFreeChallengeTimes")
                        paid = "free"
                    else:
                        item = await s.one(
                            "Item", itemMasterId=course.required_item_master_id
                        )
                        amount = course.required_amount
                        if item and item["stock"] >= amount and amount > 0:
                            await s.pay({course.required_item_master_id: amount})
                            paid = "ticket"
                        elif policy["waive_missing_course_tickets"]:
                            paid = "waived"
                        else:
                            raise Rejected("No course entry remaining")
                data = {
                    "course": course.id_,
                    "gauge": int(p.music_course_gauge_type),
                    "next": 0,
                    "rates": [],
                    "lamps": [],
                    "payment": paid,
                    "started_at": time.time_ns() // 1000,
                }
                await s.conn.conn.execute(
                    'DELETE FROM preservation_course_run WHERE "userId"=$1', s.uid
                )
                await s.conn.conn.execute(
                    'INSERT INTO preservation_course_run ("userId",data) VALUES ($1,$2)',
                    s.uid,
                    data,
                )
            else:
                if not old:
                    raise Rejected("Course has not started")
                data = old["data"]
                if (
                    data["course"] != course.id_
                    or data["next"] != index
                    or data["gauge"] != int(p.music_course_gauge_type)
                ):
                    raise Rejected("Wrong course stage")
                from helpers.daily import most_recent_reset

                if data["started_at"] < most_recent_reset(time.time_ns() // 1000):
                    raise Rejected("Course crossed daily reset")
            live_id = random.randint(1_000_000, 9_999_999_999)
            await s.conn.execute(delete_active_lives(s.uid))
            await s.conn.execute(
                create_active_live(s.uid, live_id, p.live_master_id, 0, 0, False)
            )
            await context(s, "course", d.id_, {})
        return respond(LiveUnit(u_active_live_id=live_id), present=s.present())
    except Rejected as e:
        return respond(None, faults=[fault("InvalidCourse", str(e))])


def install(app) -> None:
    """Prepend these routes so they override the base Lives/Lessons handlers."""
    count = len(app.router.routes)
    app.include_router(router)
    app.router.routes[:] = app.router.routes[count:] + app.router.routes[:count]
