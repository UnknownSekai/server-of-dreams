"""Build a LiveUnit / LiveTimeEvent from a party + masterdata.

Reversed statically from SiriusLogic.Shared:
 - sense-light / star-act progression = SenseLightsManager (_SenseLightsManager).
 - normal-live window->position = Constants.Live.BasicNotationFiredSenseRules = 1-2-3-4-5-3-2-1
   (confirmed) at floor(dur/9)*[1..8].
 - actor base status = StatusLogic.CalculateCharacterStatus (min_level_status * status_level/100).
Not yet reversed: equipment/awakening/talent stat multipliers + poster-granted wildcard lights
(both via the effect engine), neighboring sense effects, and the per-difficulty principal cap /
auto coefficient (set to functional defaults).
"""

import random
from typing import Optional

from db.user import (
    get_accessorys,
    get_albums,
    get_character_bases,
    get_characters,
    get_circle_supports,
    get_musics,
    get_party_slots,
    get_partys,
    get_posters,
)
from helpers.cache import cache
from helpers.effects import (
    added_lights,
    album_effects,
    base_correction,
    base_stat_bonus,
    bloom_effects,
    circle_effects,
    collect_slot_effects,
    max_principal,
    party_composition,
    percent_bonus,
    range_split,
    start_effects,
)
from models import (
    Actor,
    LiveStatus,
    LiveTimeEvent,
    LiveUnit,
    Sense,
    SenseCoolTime,
    SenseEffect,
    SenseTimingEvent,
    StarAct,
    TimingEvent,
)
from models.enums import MusicDifficulties, OlivierReleaseStatuses, SenseLightTypes

_MASTERS: dict = {}


def _by_id(table: str) -> dict:
    if table not in _MASTERS:
        _MASTERS[table] = {r.id_: r for r in getattr(cache, table)}
    return _MASTERS[table]


def _lights(sense_type, count: int) -> list:
    # SenseTypes and SenseLightTypes share values (Special=4, Amplification=3, ...)
    try:
        return [SenseLightTypes(int(sense_type))] * max(0, count)
    except ValueError:
        return []


_STATUS_LEVEL: dict = {}


def _status_level(level: int) -> int:
    if not _STATUS_LEVEL:
        _STATUS_LEVEL.update(
            {r.level: r.character_status_level for r in cache.character_level_master}
        )
    return _STATUS_LEVEL.get(level, 0)


_STAR_RANK_BONUS: dict = {}


def _star_rank_bonus(star_rank: int) -> float:
    # character_star_rank_master.status_bonus (percent points): rank -> bonus (rank 1 = 0.5, ...)
    if not _STAR_RANK_BONUS:
        _STAR_RANK_BONUS.update(
            {r.rank: r.status_bonus for r in cache.character_star_rank_master}
        )
    return _STAR_RANK_BONUS.get(star_rank, 0.0)


def _base_status(
    character_master,
    level: int,
    bonus: tuple = (0, 0, 0),
    percent: tuple = (0, 0, 0),
    intrinsic: float = 0.0,
) -> LiveStatus:
    # StatusLogic.CalculateCharacterStatus: character contribution =
    #   (min_level_status[c] + Base<c>Up) * status_level(level)/100 * (100 + intrinsic)/100
    # where intrinsic (percent points) = awakeningPhase*10 + star_rank.status_bonus (+ talent/bloom,
    # not yet reversed). Then CalculatePartyStatus applies the effect performance percent:
    #   final[c] = char[c] * (10000 + pct[c]) // 10000  (denominator 10000).
    mls = (
        getattr(character_master, "min_level_status", None)
        if character_master
        else None
    )
    if mls is None:
        return LiveStatus()
    sl = _status_level(level)
    f = (100.0 + intrinsic) / 100.0
    v = int((mls.vocal + bonus[0]) * sl / 100.0 * f) * (10000 + percent[0]) // 10000
    e = (
        int((mls.expression + bonus[1]) * sl / 100.0 * f)
        * (10000 + percent[1])
        // 10000
    )
    c = (
        int((mls.concentration + bonus[2]) * sl / 100.0 * f)
        * (10000 + percent[2])
        // 10000
    )
    return LiveStatus(concentration=c, expression=e, vocal=v, total_status=c + e + v)


def _party_composition(slots, chars, character_master, sense_master) -> dict:
    """Party-composition sets used to gate effect target conditions (company/attribute/etc.)."""
    cbm_master = _by_id("character_base_master")
    members: list = []
    for slot in slots:
        ch = chars.get(slot.characterId)
        cm = character_master.get(ch.characterMasterId) if ch else None
        if cm is None:
            continue
        cbm = cbm_master.get(cm.character_base_master_id)
        sm = sense_master.get(cm.sense_master_id)
        members.append(
            {
                "character_master_id": ch.characterMasterId,
                "character_base_master_id": cm.character_base_master_id,
                "company": cbm.company_master_id if cbm is not None else 0,
                "attribute": int(cm.attribute) if cm.attribute is not None else 0,
                "sense_type": sm.type if sm is not None else 0,
                "poster_id": slot.posterId,
            }
        )
    return party_composition(members)


def _position_senses(
    slots,
    chars,
    character_master,
    sense_master,
    star_act_master,
    accessories,
    posters=None,
    comp=None,
) -> dict:
    """position -> firing-sense info (id/master/cool_time/lights) incl. effect-added lights."""
    posters = posters or {}
    pos_sense: dict = {}
    for slot in slots:
        ch = chars.get(slot.characterId)
        if ch is None:
            continue
        cm = character_master.get(ch.characterMasterId)
        sm = sense_master.get(cm.sense_master_id) if cm else None
        if cm is None or sm is None:
            continue
        sam = star_act_master.get(cm.star_act_master_id) if cm else None
        effects = collect_slot_effects(
            sm,
            sam,
            ch.senseLevel,
            accessories.get(slot.accessoryId),
            posters.get(slot.posterId),
            comp,
            slot.bonusAbilityEnableFlags,
        )
        pos_sense[slot.position] = {
            "sense_master_id": cm.sense_master_id,
            "sense_id": ch.id * 100,
            "cool_time": sm.cool_time,
            "acquirable_lights": _lights(sm.type, sm.light_count)
            + added_lights(effects, sm.type),
        }
    return pos_sense


# StarActConditionMaster light fields -> SenseLightTypes (a sense grants lights of its type)
_LIGHT_FIELDS = {
    SenseLightTypes.Support: "support_light",
    SenseLightTypes.Control: "control_light",
    SenseLightTypes.Amplification: "amplification_light",
    SenseLightTypes.Special: "special_light",
}


def _star_act_condition(
    slots, chars, character_master, leader_position: int
) -> tuple[dict, int]:
    """(typed light requirements, free-light count) for the leader's star act."""
    leader = next((s for s in slots if s.position == leader_position), None)
    if leader is None:
        leader = min(slots, key=lambda s: s.position, default=None)
    ch = chars.get(leader.characterId) if leader is not None else None
    cm = character_master.get(ch.characterMasterId) if ch else None
    sam = _by_id("star_act_master").get(cm.star_act_master_id) if cm else None
    cond = (
        _by_id("star_act_condition_master").get(sam.star_act_condition_master_id)
        if sam
        else None
    )
    if cond is None:
        return {}, 0
    typed = {t: getattr(cond, f) for t, f in _LIGHT_FIELDS.items() if getattr(cond, f)}
    return typed, cond.free_light


class _SenseLightsManager:
    """Mirror of SiriusLogic.Shared...SenseTimingCalculator.SenseLightsManager (static RE).

    A granted light of the required color fills that color's slot; an off-color light fills
    a free slot if the star act needs free lights; a Variable (gray) light is a wildcard that
    always counts. When the collected total reaches the required count the star act fires and
    all lights are consumed (cleared).
    """

    def __init__(self, required: dict, required_free: int) -> None:
        self.lights: list = []  # CurrentLights (ordered) -> total_sense_lights
        self.fixed: dict = {t: 0 for t in required}  # CurrentFixedLights (per-color)
        self.free: int = 0  # CurrentFreeLightsCount
        self.required = required
        self.required_free = required_free
        self.required_count = (
            sum(required.values()) + required_free
        )  # RequiredLightCount

    def clear(self) -> None:  # ClearAllLights
        for k in self.fixed:
            self.fixed[k] = 0
        self.lights.clear()
        self.free = 0

    def grant(self, lights: list) -> tuple[bool, list]:  # GrantLights -> (fired, added)
        added: list = []
        fired = False
        for light in lights:
            if light == SenseLightTypes.Variable:  # wildcard: always counts
                self.lights.append(light)
                added.append(light)
            elif self.required.get(light, 0) > self.fixed.get(
                light, 0
            ):  # fill this color
                self.lights.append(light)
                self.fixed[light] += 1
                added.append(light)
            elif self.free < self.required_free:  # fill a free slot
                self.lights.append(light)
                self.free += 1
                added.append(light)
            else:  # off-color and no free slot -> overflow (dropped)
                continue
            if self.required_count and len(self.lights) >= self.required_count:
                self.clear()  # star act consumes the collected lights
                fired = True
                break
        return fired, added


def _live_time_event(
    pos_sense: dict, music_time_second: int, sense_notation, star_act_condition
) -> LiveTimeEvent:
    required, required_free = star_act_condition
    if sense_notation is not None:
        windows = [(d.timing_second, d.position) for d in sense_notation.details]
    else:
        # normal live: 8 windows evenly spread over the song's stated duration, firing in
        # the in-game unit formation order 1-2-3-4-5-3-2-1.
        step = music_time_second // 9
        formation = (1, 2, 3, 4, 5, 3, 2, 1)
        windows = [(step * i, formation[i - 1]) for i in range(1, 9)]
    windows.sort()

    mgr = _SenseLightsManager(required, required_free)
    last_act: dict = {}
    timings: list = []
    for sec, pos in windows:
        sense = pos_sense.get(pos)
        prev = last_act.get(pos)
        cool = sense["cool_time"] if sense else 0
        # a window whose sense is still on cool_time can't fire -> all collected lights lost
        lost = sense is None or (prev is not None and (sec - prev) < cool)
        if lost:
            mgr.clear()
            fired, added = False, []
        else:
            last_act[pos] = sec
            fired, added = mgr.grant(list(sense["acquirable_lights"]))
        event = TimingEvent(
            total_sense_lights=list(mgr.lights),
            grant_sense_lights=added,
            is_star_act=fired,
            lost_lights=lost,
            acquirable_lights=list(sense["acquirable_lights"]) if sense else [],
            sense_ids=[sense["sense_id"]] if sense else [],
            sense_voice_ids=[],
            sense_master_id=sense["sense_master_id"] if sense else 0,
        )
        timings.append(SenseTimingEvent(timing_seconds=sec, position=pos, event=event))
    cool_times = [
        SenseCoolTime(position=p, cool_time=s["cool_time"])
        for p, s in sorted(pos_sense.items())
    ]
    return LiveTimeEvent(timings=timings, cool_times=cool_times)


async def build_live_time_event(
    conn,
    user_id: int,
    party_id: int,
    music_master_id: int,
    sense_notation_master_id: Optional[int] = None,
) -> LiveTimeEvent:
    """Sense timing schedule for a live. ``sense_notation_master_id=None`` -> normal live
    (spread over the song duration); otherwise from ``SenseNotationMaster.details``."""
    slots = [
        s for s in await conn.fetch(get_party_slots(user_id)) if s.partyId == party_id
    ]
    chars = {c.id: c for c in await conn.fetch(get_characters(user_id))}
    accessories = {a.id: a for a in await conn.fetch(get_accessorys(user_id))}
    posters = {p.id: p for p in await conn.fetch(get_posters(user_id))}
    leader_position = next(
        (
            p.leaderPosition
            for p in await conn.fetch(get_partys(user_id))
            if p.id == party_id
        ),
        1,
    )
    character_master = _by_id("character_master")
    sense_master = _by_id("sense_master")
    comp = _party_composition(slots, chars, character_master, sense_master)
    pos_sense = _position_senses(
        slots,
        chars,
        character_master,
        sense_master,
        _by_id("star_act_master"),
        accessories,
        posters,
        comp,
    )
    music = _by_id("music_master").get(music_master_id)
    duration = music.music_time_second if music is not None else 0
    snm = (
        _by_id("sense_notation_master").get(sense_notation_master_id)
        if sense_notation_master_id
        else None
    )
    condition = _star_act_condition(slots, chars, character_master, leader_position)
    return _live_time_event(pos_sense, duration, snm, condition)


async def build_live_unit(conn, user_id: int, party_id: int, live_master_id: int):
    """Returns (LiveUnit, active_live_id). See module docstring for the placeholder parts."""
    slots = sorted(
        (
            s
            for s in await conn.fetch(get_party_slots(user_id))
            if s.partyId == party_id
        ),
        key=lambda s: s.position,
    )
    chars = {c.id: c for c in await conn.fetch(get_characters(user_id))}
    bases = {b.id: b for b in await conn.fetch(get_character_bases(user_id))}
    accessories = {a.id: a for a in await conn.fetch(get_accessorys(user_id))}
    posters = {p.id: p for p in await conn.fetch(get_posters(user_id))}
    album_level = next((a.level for a in await conn.fetch(get_albums(user_id))), 0)
    circle_levels = {
        cs.company: cs.level for cs in await conn.fetch(get_circle_supports(user_id))
    }
    leader_position = next(
        (
            p.leaderPosition
            for p in await conn.fetch(get_partys(user_id))
            if p.id == party_id
        ),
        1,
    )
    character_master = _by_id("character_master")
    sense_master = _by_id("sense_master")
    star_act_master = _by_id("star_act_master")
    comp = _party_composition(slots, chars, character_master, sense_master)

    # pass 1: collect each slot's full effects and aggregate All-range effects across the party
    # (a Leader poster boosts everyone). Self/None effects stay slot-local. Album effects are
    # party-wide (unlocked by album level).
    slot_effects: dict = {}
    party_all: list = album_effects(album_level, comp)
    for slot in slots:
        ch = chars.get(slot.characterId)
        cm = character_master.get(ch.characterMasterId) if ch else None
        sm = sense_master.get(cm.sense_master_id) if cm else None
        sam = star_act_master.get(cm.star_act_master_id) if cm else None
        eff = collect_slot_effects(
            sm,
            sam,
            ch.senseLevel if ch else 0,
            accessories.get(slot.accessoryId),
            posters.get(slot.posterId),
            comp,
            slot.bonusAbilityEnableFlags,
        )
        if (
            cm is not None and ch is not None
        ):  # talent-bloom effects (phase <= talentStage)
            eff = eff + bloom_effects(
                cm.bloom_bonus_group_master_id, ch.talentStage, comp
            )
        slot_effects[slot.position] = eff
        party_all += range_split(eff)[1]

    # MaxPrincipal = base + the party's passive PrincipalGaugeLimitUp effects (each counted once:
    # party-wide All-range + every slot's own effects).
    principal_max = max_principal(
        party_all + [e for effs in slot_effects.values() for e in range_split(effs)[0]]
    )

    actors: dict = {}
    senses: list = []
    start_effects_all: list = []
    star_act = StarAct()
    for slot in slots:
        ch = chars.get(slot.characterId)
        if ch is None:
            continue
        base = bases.get(ch.characterBaseId)
        sec = (
            bases.get(ch.secondaryCharacterBaseId)
            if ch.secondaryCharacterBaseId
            else None
        )
        cm = character_master.get(ch.characterMasterId)
        sm = sense_master.get(cm.sense_master_id) if cm else None
        sam = star_act_master.get(cm.star_act_master_id) if cm else None
        full = slot_effects.get(slot.position, [])
        # for this actor's stats/lights: its own (Self/None) effects + every All-range effect
        # + the actor's company circle-support effects.
        cbm = (
            _by_id("character_base_master").get(cm.character_base_master_id)
            if cm
            else None
        )
        circle = (
            circle_effects(cbm.company_master_id, circle_levels, comp) if cbm else []
        )
        effects = range_split(full)[0] + party_all + circle

        # intrinsic factor (percent points on the char base): awakening phase (10%/phase) +
        # star rank status bonus + bloom BaseCorrection effects.
        intrinsic = (
            ch.awakeningPhase * 10
            + _star_rank_bonus(base.starRank if base else 0)
            + base_correction(effects)
        )
        status = _base_status(
            cm, ch.level, base_stat_bonus(effects), percent_bonus(effects), intrinsic
        )
        actors[slot.position] = Actor(
            id_=ch.id,
            character_base_master_id=base.characterBaseMasterId if base else 0,
            character_master_id=ch.characterMasterId,
            awakening_phase=ch.awakeningPhase,
            talent_stage=ch.talentStage,
            position=slot.position,
            sense_level=ch.senseLevel,
            base_status=status,
            current_status=status.model_copy(),
            display_awakening_status=ch.displayAwakeningStatus,
            secondary_character_base_master_id=(
                sec.characterBaseMasterId if sec else None
            ),
            secondary_sense_level=ch.secondarySenseLevel,
            selection_type=ch.selectionType,
        )
        if cm is not None and sm is not None:
            senses.append(
                Sense(
                    id_=ch.id * 100,
                    actor_id=ch.id,
                    cool_time=sm.cool_time,
                    sense_type=sm.type,
                    acquirable_lights=_lights(sm.type, sm.light_count)
                    + added_lights(effects, sm.type),
                    sense_effect=SenseEffect(
                        score_factor=sm.acquirable_score_percent,
                        principal=0,
                        branch_condition=int(sm.branch_condition1),
                    ),
                    sense_master_id=cm.sense_master_id,
                    original_actor_id=ch.id,
                )
            )
        # start effects emitted once from their source slot (the effect's own range targets who)
        start_effects_all += start_effects(full, ch.id, len(start_effects_all))
        if (
            slot.position == leader_position and sam is not None
        ):  # leader drives the star act
            star_act = StarAct(
                score_factor=sam.acquirable_score_percent,
                actor_id=ch.id,
                branch_condition=int(sam.branch_condition1),
            )

    # sum of every actor's current status total (0 while status is a placeholder)
    total_status = sum(a.current_status.total_status for a in actors.values())

    lm = _by_id("live_master").get(live_master_id)

    # The Stella->Olivier intro marks how the chart was entered, not play history: it plays
    # when the live was launched by holding the Stella button, and Challengeable is the only
    # status that gesture is offered on. Purchasable means an Olivier clear at this level or
    # above has put the chart in the shop instead, so it has to be bought, and Released picks
    # straight off the difficulty list -- neither shows a transition. It repeats for as long
    # as the chart stays Challengeable. StartLivePayload carries no field for the gesture
    # itself (it ends at trial_party_event_stage_master_id), so status is all there is to go
    # on.
    is_first_olivier = False
    if lm is not None and int(lm.difficulty) == int(MusicDifficulties.Olivier):
        music = next(
            (
                m
                for m in await conn.fetch(get_musics(user_id))
                if m.musicMasterId == lm.music_master_id
            ),
            None,
        )
        is_first_olivier = music is not None and music.olivierReleaseStatus == int(
            OlivierReleaseStatuses.Challengeable
        )

    # normal live: time events spread over the song duration (no sense notation).
    # TimeEvents is keyed by the timing second; the value is that window's TimingEvent.
    music = _by_id("music_master").get(lm.music_master_id) if lm is not None else None
    pos_sense = _position_senses(
        slots,
        chars,
        character_master,
        sense_master,
        star_act_master,
        accessories,
        posters,
        comp,
    )
    condition = _star_act_condition(slots, chars, character_master, leader_position)
    lte = _live_time_event(
        pos_sense, music.music_time_second if music is not None else 0, None, condition
    )
    time_events = {t.timing_seconds: t.event for t in lte.timings}
    # lights needed for a star act = the leader's typed requirements + free lights
    star_act_sense_light_count = sum(condition[0].values()) + condition[1]

    live_id = random.randint(1_000_000, 9_999_999_999)
    unit = LiveUnit(
        actors=actors,
        time_events=time_events,
        possible_senses=senses,
        start_effects=start_effects_all,
        star_act=star_act,
        total_status=total_status,
        star_act_sense_light_count=star_act_sense_light_count,
        max_principal=principal_max,
        # base_score_difficulty_auto_coefficient: per-difficulty, server-set (tutorial 0.95).
        base_score_difficulty_auto_coefficient=0.95,
        is_first_play_olivier=is_first_olivier,
        u_active_live_id=live_id,
    )
    return unit, live_id
