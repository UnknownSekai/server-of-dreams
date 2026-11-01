"""Effect engine: collect a party slot's effects from masterdata and apply them.

- Effect collection across sources: equipped accessories (fixed + rolled effects), posters
  (unlocked abilities evaluated at level + breakthroughPhase), talent-bloom bonuses, circle supports,
  album party-wide bonuses, leader sense effects, and intrinsic character traits.
- Party composition matching: checks company, attribute, character, sense type, and trigger types
  (AllMemberBelongingCompany, MaxMemberBelongingCompanyCount, MaxMemberBelongingAttributeCount).
- Target range handling: Self/None stay slot-local; All-range effects are filtered by target actor
  conditions before being applied to individual members.
- Source priority capping: Album -> Poster -> Accessory -> BloomBonus -> Other -> LeaderSense
  to allocate percentage limits (StatusLimitUp / PerformanceLimitUp) and preserve integer truncation parity.
- Live start effects and lights: extracts StartLive AddSenseLight* into opening pool and handles
  DecreaseRequire*Light for star act requirements.
"""

from collections import Counter
from typing import NamedTuple, Optional

from helpers.cache import cache
from models import Effect, EffectTargetValue
from models.enums import (
    CalculationTypes,
    EffectSourceTypes,
    EffectTargetRanges,
    EffectTypes,
    FireTimingTypes,
    PosterEffectTypes,
    SenseLightTypes,
    TriggerType,
)


class AppliedEffect(NamedTuple):
    """One collected effect: its master, the level used to pick the detail value, and its origin."""

    master: object
    level: int
    source: EffectSourceTypes = EffectSourceTypes.Other


_EM: dict = {}
_AEM: dict = {}
_AM: dict = {}
_LSM: dict = {}


def _em(effect_master_id: int):
    if not _EM:
        _EM.update({e.id_: e for e in cache.effect_master})
    return _EM.get(effect_master_id)


def _aem(accessory_effect_id: int):
    if not _AEM:
        _AEM.update({e.id_: e for e in cache.accessory_effect_master})
    return _AEM.get(accessory_effect_id)


def _am(accessory_master_id: int):
    if not _AM:
        _AM.update({a.id_: a for a in cache.accessory_master})
    return _AM.get(accessory_master_id)


def _lsm(leader_sense_master_id: int):
    if not _LSM:
        _LSM.update({l.id_: l for l in cache.leader_sense_master})
    return _LSM.get(leader_sense_master_id)


def _detail_value(em, level: int) -> float:
    # pick the detail at the highest level <= source level (fallback: first detail)
    best = None
    for d in em.details or []:
        if d.level <= level and (best is None or d.level > best.level):
            best = d
    if best is None and em.details:
        best = em.details[0]
    return best.value if best is not None else 0.0


# EffectConditions -> the party-composition set it checks (ValidateTargetCondition: Where+Any over
# the party -> a condition passes when the party contains a matching member). NeighborPosition(7)
# and CharacterBaseGroup(8) need per-position/group data and are left un-gated (always allowed).
_COND_KEY = {
    1: "char_bases",
    2: "companies",
    3: "attributes",
    4: "sense_types",
    5: "characters",
    6: "posters",
}


def party_composition(members: list) -> dict:
    """members: dicts with character_master_id/character_base_master_id/company/attribute/
    sense_type/poster_id. Returns the sets and counts ValidateTargetCondition matches against.
    """
    companies = [m["company"] for m in members]
    attributes = [m["attribute"] for m in members]
    return {
        "char_bases": {m["character_base_master_id"] for m in members},
        "companies": set(companies),
        "attributes": set(attributes),
        "characters": {m["character_master_id"] for m in members},
        "sense_types": {int(m["sense_type"]) for m in members},
        "posters": {m["poster_id"] for m in members if m["poster_id"]},
        "company_counts": Counter(companies),
        "attribute_counts": Counter(attributes),
        "member_count": len(members),
    }


def _conditions_met(em, comp: Optional[dict]) -> bool:
    if comp is None:
        return True
    for c in em.conditions or []:
        key = _COND_KEY.get(int(c.condition))
        if key is None:  # NeighborPosition / CharacterBaseGroup -> not modeled -> allow
            continue
        if c.value not in comp[key]:
            return False
    for tr in em.triggers or []:
        t = int(tr.trigger)
        val = tr.value
        if t == TriggerType.AllMemberBelongingCompany:
            if comp.get("company_counts", {}).get(val, 0) != comp.get(
                "member_count", 0
            ):
                return False
        elif t == TriggerType.MaxMemberBelongingCompanyCount:
            max_comp = max(comp.get("company_counts", {}).values(), default=0)
            if max_comp < val:
                return False
        elif t == TriggerType.MaxMemberBelongingAttributeCount:
            max_attr = max(comp.get("attribute_counts", {}).values(), default=0)
            if max_attr < val:
                return False
        elif t == TriggerType.Company:
            if val not in comp.get("companies", set()):
                return False
        elif t == TriggerType.Attribute:
            if val not in comp.get("attributes", set()):
                return False
        elif t == TriggerType.CharacterBase:
            if val not in comp.get("char_bases", set()):
                return False
        elif t == TriggerType.SenseType:
            if int(val) not in comp.get("sense_types", set()):
                return False
    return True


_POSTER_ABILITIES: dict = {}


def _poster_abilities(poster_master_id: int) -> list:
    if not _POSTER_ABILITIES:
        for pa in cache.poster_ability_master:
            _POSTER_ABILITIES.setdefault(pa.poster_master_id, []).append(pa)
    return _POSTER_ABILITIES.get(poster_master_id, [])


def collect_slot_effects(
    sense_master,
    star_act_master,
    sense_level: int,
    accessory,
    poster=None,
    comp: Optional[dict] = None,
    bonus_flags: int = 0,
    is_leader: bool = False,
) -> list:
    """Returns [(EffectMaster, level, EffectSourceTypes)] for one slot from its resolvable sources,
    keeping only effects whose target conditions are met by the party composition ``comp``.
    """
    raw: list = []
    if sense_master is not None:
        for eo in sense_master.pre_effects or []:
            em = _em(eo.effect_master_id)
            if em is not None:
                raw.append(AppliedEffect(em, sense_level, EffectSourceTypes.Other))
        for br in sense_master.branches or []:
            for eo in br.branch_effects or []:
                em = _em(eo.effect_master_id)
                if em is not None:
                    raw.append(AppliedEffect(em, sense_level, EffectSourceTypes.Other))
    if star_act_master is not None:
        for eo in star_act_master.pre_effects or []:
            em = _em(eo.effect_master_id)
            if em is not None:
                raw.append(AppliedEffect(em, sense_level, EffectSourceTypes.Other))
    if accessory is not None:
        am = _am(accessory.accessoryMasterId)
        if am is not None:
            for faeid in am.fixed_accessory_effects or []:
                ae = _aem(faeid)
                em = _em(ae.effect_master_id) if ae is not None else None
                if em is not None:
                    raw.append(
                        AppliedEffect(em, accessory.level, EffectSourceTypes.Accessory)
                    )
        for aeid in accessory.accessoryEffects or []:
            ae = _aem(aeid)
            em = _em(ae.effect_master_id) if ae is not None else None
            if em is not None:
                raw.append(
                    AppliedEffect(em, accessory.level, EffectSourceTypes.Accessory)
                )
    if poster is not None:
        # poster abilities unlocked at the poster's level and enabled by the slot's
        # BonusAbilityEnableFlags (bit frame_number-1). bonus_flags==0 -> treat as all enabled.
        p_lvl = poster.level + getattr(poster, "breakthroughPhase", 0)
        for pa in _poster_abilities(poster.posterMasterId):
            if pa.type == PosterEffectTypes.Leader and not is_leader:
                continue
            if poster.level < pa.release_level_at:
                continue
            if bonus_flags and not (bonus_flags >> (pa.frame_number - 1)) & 1:
                continue
            for br in pa.branches or []:
                for eo in br.branch_effects or []:
                    em = _em(eo.effect_master_id)
                    if em is not None:
                        raw.append(AppliedEffect(em, p_lvl, EffectSourceTypes.Poster))
    return [e for e in raw if _conditions_met(e.master, comp)]


# EffectConditions (1..5) -> the actor attribute that must equal the condition value.
_ACTOR_COND_KEY = {
    1: "character_base_master_id",
    2: "company",
    3: "attribute",
    4: "sense_type",
    5: "character_master_id",
}


def filter_target_effects(effects: list, actor_dict: dict) -> list:
    """Filter effects whose target conditions match the individual actor."""
    return [
        e
        for e in effects
        if all(
            actor_dict.get(_ACTOR_COND_KEY[int(c.condition)]) == c.value
            for c in e.master.conditions or []
            if int(c.condition) in _ACTOR_COND_KEY
        )
    ]


def range_split(effects: list) -> tuple:
    """(self_or_none effects, all-range effects). All-range effects apply to every actor
    (EffectTargetRanges.All == 2), so they are aggregated party-wide."""
    own = [e for e in effects if int(e.master.range) != int(EffectTargetRanges.All)]
    every = [e for e in effects if int(e.master.range) == int(EffectTargetRanges.All)]
    return own, every


def album_effects(album_level: int, comp: Optional[dict] = None) -> list:
    """Party-wide effects unlocked by the user's album level (album_effect_master.level)."""
    out: list = []
    for ae in cache.album_effect_master:
        if ae.level <= album_level:
            em = _em(ae.effect_master_id)
            if em is not None:
                out.append(AppliedEffect(em, album_level, EffectSourceTypes.Album))
    return [e for e in out if _conditions_met(e.master, comp)]


_BLOOM_GROUP: dict = {}


def bloom_effects(
    bloom_group_master_id, bloom_stage: int, comp: Optional[dict] = None
) -> list:
    """Character talent-bloom effects: character_bloom_bonus_group_master.bloom_bonuses whose
    phase <= the character's bloom stage (talentStage). Phases stack (e.g. 5x PerformanceUp).
    """
    if not _BLOOM_GROUP:
        _BLOOM_GROUP.update(
            {g.id_: g for g in cache.character_bloom_bonus_group_master}
        )
    g = _BLOOM_GROUP.get(bloom_group_master_id)
    if g is None:
        return []
    out: list = []
    for bb in g.bloom_bonuses or []:
        if bb.phase <= bloom_stage:
            em = _em(bb.effect_master_id)
            if em is not None:
                out.append(AppliedEffect(em, bloom_stage, EffectSourceTypes.BloomBonus))
    return [e for e in out if _conditions_met(e.master, comp)]


_CIRCLE_BY_COMPANY: dict = {}


def circle_effects(
    company: int, circle_levels: dict, comp: Optional[dict] = None
) -> list:
    """Effects for an actor of ``company`` from the user's circle support (per-company):
    circle_support_company_level_detail_master rows of that company up to the user's level.
    """
    if not _CIRCLE_BY_COMPANY:
        for cd in cache.circle_support_company_level_detail_master:
            _CIRCLE_BY_COMPANY.setdefault(int(cd.company), []).append(cd)
    level = circle_levels.get(company, 0)
    out: list = []
    for cd in _CIRCLE_BY_COMPANY.get(company, []):
        if cd.level <= level:
            em = _em(cd.effect_master_id)
            if em is not None:
                # No dedicated EffectSourceTypes member for circle support; it is capped as Other.
                out.append(AppliedEffect(em, cd.level, EffectSourceTypes.Other))
    return [e for e in out if _conditions_met(e.master, comp)]


def _leader_condition_met(detail, member_cats: set) -> bool:
    """A LeaderSense detail applies when it has no conditions, or when any one condition has all of
    its listed categories on the member (a condition listing no category always matches).
    """
    if not detail.conditions:
        return True
    for cond in detail.conditions:
        req = [
            cid
            for cid in (getattr(cond, f"category_master_id{i}") for i in range(1, 6))
            if cid is not None
        ]
        if all(cid in member_cats for cid in req):
            return True
    return False


def leader_sense_effects(leader_cm, member_cm) -> list:
    """Effects granted to member_cm by leader_cm's LeaderSenseMaster.
    Returns [AppliedEffect(EffectMaster, level=1, EffectSourceTypes.LeaderSense)].
    """
    if leader_cm is None or not leader_cm.leader_sense_master_id or member_cm is None:
        return []
    lsm = _lsm(leader_cm.leader_sense_master_id)
    if lsm is None or not lsm.details:
        return []
    member_cats = {c.category_master_id for c in (member_cm.categories or [])}
    out: list = []
    for detail in lsm.details:
        em = _em(detail.effect_master_id)
        if em is not None and _leader_condition_met(detail, member_cats):
            out.append(AppliedEffect(em, 1, EffectSourceTypes.LeaderSense))
    return out


def sum_by_type_and_source(
    effects: list,
    effect_type,
    calc_type: Optional[int] = None,
    source_type: Optional[int] = None,
) -> float:
    """GetEffectValue: sum of an effect type's detail values, optionally filtered by
    calculation_type (CalculationTypes) and source_type (EffectSourceTypes)."""
    t = int(effect_type)
    c = int(calc_type) if calc_type is not None else None
    src = int(source_type) if source_type is not None else None
    return sum(
        _detail_value(e.master, e.level)
        for e in effects
        if int(e.master.type) == t
        and (c is None or int(e.master.calculation_type) == c)
        and (src is None or int(e.source) == src)
    )


def sum_by_type(effects: list, effect_type, calc_type: Optional[int] = None) -> float:
    """sum_by_type_and_source without the source filter."""
    return sum_by_type_and_source(effects, effect_type, calc_type)


def _fixed_sums(effects: list, effect_types: tuple) -> tuple:
    return tuple(
        int(sum_by_type(effects, t, CalculationTypes.FixedAddition))
        for t in effect_types
    )


def base_stat_bonus(effects: list) -> tuple:
    """Per-component flat Base<Component>Up sums (FixedAddition) -> (vocal, expression, concentration)."""
    return _fixed_sums(
        effects,
        (
            EffectTypes.BaseVocalUp,
            EffectTypes.BaseExpressionUp,
            EffectTypes.BaseConcentrationUp,
        ),
    )


def component_flat_bonus(effects: list) -> tuple:
    """Per-component flat <Component>Up sums (FixedAddition) -> (vocal, expression, concentration).
    E.g. flat stat additions from equipped accessories, posters, or circle/album flat bonuses.
    """
    return _fixed_sums(
        effects,
        (EffectTypes.VocalUp, EffectTypes.ExpressionUp, EffectTypes.ConcentrationUp),
    )


_BASE_MAX_PRINCIPAL = (
    1000  # Constants base (= TutorialMaxPrincipal); PrincipalGaugeLimitUp raises it
)


def max_principal(effects: list) -> int:
    """LiveUnit.MaxPrincipal = base 1000 raised by the party's always-on PrincipalGaugeLimitUp
    effects (effect 41): FixedAddition adds flat, PercentageAddition scales the base (/10000).
    Sense/StarAct-timed ones raise it during play (IncreaseMax), not the initial max."""
    flat = 0.0
    pct = 0.0
    for e in effects:
        em, lv = e.master, e.level
        if int(em.type) != int(EffectTypes.PrincipalGaugeLimitUp):
            continue
        if int(em.fire_timing_type) != int(FireTimingTypes.Passive):
            continue
        v = _detail_value(em, lv)
        if int(em.calculation_type) == int(CalculationTypes.FixedAddition):
            flat += v
        elif int(em.calculation_type) == int(
            CalculationTypes.PercentageAddition
        ):  # /10000
            pct += v
    return int(_BASE_MAX_PRINCIPAL * (1 + pct / 10000) + flat)


def base_correction(effects: list) -> float:
    """BaseCorrection (type 4, PercentageAddition, Self) -> percent points on the character base
    (the leaf's w5 term; value 200 = +2%). Bloom 'performance up' bonuses are BaseCorrection.
    """
    return (
        sum_by_type(
            effects, EffectTypes.BaseCorrection, CalculationTypes.PercentageAddition
        )
        / 100.0
    )


# Constants.Character: caps on the status/performance percent, raised by the matching *LimitUp.
_STATUS_PERCENT_LIMIT = 20000
_PERFORMANCE_PERCENT_LIMIT = 20000

# Source priority order for applying caps and rounding
SOURCE_PRIORITY = (
    EffectSourceTypes.Album,
    EffectSourceTypes.Poster,
    EffectSourceTypes.Accessory,
    EffectSourceTypes.BloomBonus,
    EffectSourceTypes.Other,
    EffectSourceTypes.LeaderSense,
)


def component_percent_bonuses_by_source(effects: list) -> dict:
    """Per-source component percentage bonuses (PercentageAddition, calc_type 1) in basis units
    (10000 = 100%), capped in source priority order:
    Album -> Poster -> Accessory -> BloomBonus -> Other -> LeaderSense.
    Returns {source_type: (vocal_bps, expression_bps, concentration_bps)}.
    """
    v_cap = _STATUS_PERCENT_LIMIT + sum_by_type(
        effects, EffectTypes.VocalLimitUp, CalculationTypes.PercentageAddition
    )
    e_cap = _STATUS_PERCENT_LIMIT + sum_by_type(
        effects, EffectTypes.ExpressionLimitUp, CalculationTypes.PercentageAddition
    )
    c_cap = _STATUS_PERCENT_LIMIT + sum_by_type(
        effects, EffectTypes.ConcentrationLimitUp, CalculationTypes.PercentageAddition
    )

    res: dict = {}
    for src in SOURCE_PRIORITY:
        s_int = int(src)
        v_raw = sum_by_type_and_source(
            effects, EffectTypes.VocalUp, CalculationTypes.PercentageAddition, s_int
        )
        e_raw = sum_by_type_and_source(
            effects,
            EffectTypes.ExpressionUp,
            CalculationTypes.PercentageAddition,
            s_int,
        )
        c_raw = sum_by_type_and_source(
            effects,
            EffectTypes.ConcentrationUp,
            CalculationTypes.PercentageAddition,
            s_int,
        )

        v_val = min(v_raw, v_cap)
        e_val = min(e_raw, e_cap)
        c_val = min(c_raw, c_cap)

        v_cap -= v_val
        e_cap -= e_val
        c_cap -= c_val

        if v_val or e_val or c_val:
            res[s_int] = (int(v_val), int(e_val), int(c_val))
    return res


def performance_percent_bonuses_by_source(effects: list) -> dict:
    """Per-source performance percentage bonuses (PercentageAddition, calc_type 1) in basis units
    (10000 = 100%), capped in source priority order.
    Returns {source_type: perf_bps}.
    """
    cap = _PERFORMANCE_PERCENT_LIMIT + sum_by_type(
        effects, EffectTypes.PerformanceLimitUp, CalculationTypes.PercentageAddition
    )
    res: dict = {}
    for src in SOURCE_PRIORITY:
        s_int = int(src)
        raw = sum_by_type_and_source(
            effects,
            EffectTypes.PerformanceUp,
            CalculationTypes.PercentageAddition,
            s_int,
        )
        val = min(raw, cap)
        cap -= val
        if val:
            res[s_int] = int(val)
    return res


def final_performance_multiplier(effects: list) -> float:
    """Multiplication factor from CalculationTypes.Multiplication (e.g. FinalPerformanceUpCancelSense)."""
    mult = 1.0
    for e in effects:
        em = e.master
        lvl = e.level
        if (
            getattr(em, "calculation_type", None) == CalculationTypes.Multiplication
            and getattr(em, "type", None) == EffectTypes.FinalPerformanceUpCancelSense
        ):
            val = _detail_value(em, lvl)
            if val > 0:
                mult *= val / 100.0
    return mult


def _light_of(effect_type: int, sense_type) -> Optional[SenseLightTypes]:
    if effect_type == int(EffectTypes.AddSenseLightSelf):
        try:
            return SenseLightTypes(int(sense_type))
        except ValueError:
            return SenseLightTypes.Variable
    if (
        int(EffectTypes.AddSenseLightVariable)
        <= effect_type
        <= int(EffectTypes.AddSenseLightSpecial)
    ):
        return SenseLightTypes(effect_type - int(EffectTypes.AddSenseLightVariable))
    return None


def added_lights(effects: list, sense_type) -> list:
    """Extra lights granted to a sense by passive AddSenseLight* effects."""
    lights: list = []
    for e in effects:
        em, lv = e.master, e.level
        if int(em.fire_timing_type) == int(FireTimingTypes.StartLive):
            continue
        light = _light_of(int(em.type), sense_type)
        if light is not None:
            lights += [light] * max(0, int(_detail_value(em, lv)))
    return lights


def start_lights(effects: list, sense_type: int = 0) -> list:
    """Lights granted at live start by StartLive AddSenseLight* effects."""
    lights: list = []
    for e in effects:
        em, lv = e.master, e.level
        if int(em.fire_timing_type) != int(FireTimingTypes.StartLive):
            continue
        light = _light_of(int(em.type), sense_type)
        if light is not None:
            lights += [light] * max(0, int(_detail_value(em, lv)))
    return lights


_DECREASE_LIGHT_TYPE_MAP = {
    int(EffectTypes.DecreaseRequireSupportLight): SenseLightTypes.Support,
    int(EffectTypes.DecreaseRequireControlLight): SenseLightTypes.Control,
    int(EffectTypes.DecreaseRequireAmplificationLight): SenseLightTypes.Amplification,
    int(EffectTypes.DecreaseRequireSpecialLight): SenseLightTypes.Special,
}


def decrease_require_lights(effects: list) -> dict:
    """Light count reductions for star act from DecreaseRequire*Light effects."""
    reductions: dict = {}
    for e in effects:
        em, lv = e.master, e.level
        light_type = _DECREASE_LIGHT_TYPE_MAP.get(int(em.type))
        if light_type is not None:
            reductions[light_type] = reductions.get(light_type, 0) + int(
                _detail_value(em, lv)
            )
    return reductions


def start_effects(effects: list, actor_id: int, start_order: int = 0) -> list:
    """Effects with FireTimingTypes.StartLive as LiveUnit.StartEffects Effect entities."""
    result: list = []
    order = start_order
    for e in effects:
        em, lv = e.master, e.level
        if int(em.fire_timing_type) != int(FireTimingTypes.StartLive):
            continue
        order += 1
        value = _detail_value(em, lv)
        # range Self -> this actor; All -> every actor (target_actor_id=None)
        target = actor_id if int(em.range) == int(EffectTargetRanges.Self) else None
        result.append(
            Effect(
                order=order,
                master_id=em.id_,
                effect_types=em.type,
                targets=[EffectTargetValue(target_actor_id=target, value=value)],
                duration=em.duration_second,
            )
        )
    return result
