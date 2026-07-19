"""Effect engine: collect a party slot's effects from masterdata and apply them.

Reversed from SiriusLogic.Shared.PartyStatusCalculator (see scratchpad/RE_NOTES.md):
each source contributes EffectMaster references; an effect's value = its detail value at the
source level, and modifiers are the per-type sum (``GetEffectValue``). ``fire_timing_type``
routes where an effect applies: StartLive -> LiveUnit.StartEffects; Passive stat types ->
base status; AddSenseLight* -> a sense's granted lights.

Sources wired here: the actor's sense (pre_effects + branch effects), star act pre_effects,
and the equipped accessory. Poster / album / circle-support / talent / awakening remain TODO.
"""

from typing import Optional

from helpers.cache import cache
from models import Effect, EffectTargetValue
from models.enums import EffectTypes, FireTimingTypes, SenseLightTypes

_EM: dict = {}
_AEM: dict = {}


def _em(effect_master_id: int):
    if not _EM:
        _EM.update({e.id_: e for e in cache.effect_master})
    return _EM.get(effect_master_id)


def _aem(accessory_effect_id: int):
    if not _AEM:
        _AEM.update({e.id_: e for e in cache.accessory_effect_master})
    return _AEM.get(accessory_effect_id)


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
    sense_type/poster_id. Returns the sets ValidateTargetCondition matches against."""
    return {
        "char_bases": {m["character_base_master_id"] for m in members},
        "companies": {m["company"] for m in members},
        "attributes": {m["attribute"] for m in members},
        "characters": {m["character_master_id"] for m in members},
        "sense_types": {int(m["sense_type"]) for m in members},
        "posters": {m["poster_id"] for m in members if m["poster_id"]},
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
) -> list:
    """Returns [(EffectMaster, level)] for one slot from its resolvable sources, keeping only
    effects whose target conditions are met by the party composition ``comp``."""
    raw: list = []
    if sense_master is not None:
        for eo in sense_master.pre_effects or []:
            em = _em(eo.effect_master_id)
            if em is not None:
                raw.append((em, sense_level))
        for br in sense_master.branches or []:
            for eo in br.branch_effects or []:
                em = _em(eo.effect_master_id)
                if em is not None:
                    raw.append((em, sense_level))
    if star_act_master is not None:
        for eo in star_act_master.pre_effects or []:
            em = _em(eo.effect_master_id)
            if em is not None:
                raw.append((em, sense_level))
    if accessory is not None:
        for aeid in accessory.accessoryEffects or []:
            ae = _aem(aeid)
            em = _em(ae.effect_master_id) if ae is not None else None
            if em is not None:
                raw.append((em, accessory.level))
    if poster is not None:
        # poster abilities unlocked at the poster's level and enabled by the slot's
        # BonusAbilityEnableFlags (bit frame_number-1). bonus_flags==0 -> treat as all enabled.
        for pa in _poster_abilities(poster.posterMasterId):
            if poster.level < pa.release_level_at:
                continue
            if bonus_flags and not (bonus_flags >> (pa.frame_number - 1)) & 1:
                continue
            for br in pa.branches or []:
                for eo in br.branch_effects or []:
                    em = _em(eo.effect_master_id)
                    if em is not None:
                        raw.append((em, poster.level))
    return [(em, lv) for em, lv in raw if _conditions_met(em, comp)]


def range_split(effects: list) -> tuple:
    """(self_or_none effects, all-range effects). All-range effects apply to every actor
    (EffectTargetRanges.All == 2), so they are aggregated party-wide."""
    own = [(em, lv) for em, lv in effects if int(em.range) != 2]
    every = [(em, lv) for em, lv in effects if int(em.range) == 2]
    return own, every


def album_effects(album_level: int, comp: Optional[dict] = None) -> list:
    """Party-wide effects unlocked by the user's album level (album_effect_master.level)."""
    out: list = []
    for ae in cache.album_effect_master:
        if ae.level <= album_level:
            em = _em(ae.effect_master_id)
            if em is not None:
                out.append((em, album_level))
    return [(em, lv) for em, lv in out if _conditions_met(em, comp)]


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
                out.append((em, bloom_stage))
    return [(em, lv) for em, lv in out if _conditions_met(em, comp)]


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
                out.append((em, cd.level))
    return [(em, lv) for em, lv in out if _conditions_met(em, comp)]


def sum_by_type(effects: list, effect_type) -> float:
    """GetEffectValue: sum of an effect type's detail values across the collected effects."""
    t = int(effect_type)
    return sum(_detail_value(em, lv) for em, lv in effects if int(em.type) == t)


def base_stat_bonus(effects: list) -> tuple:
    """Per-component flat Base<Component>Up sums -> (vocal, expression, concentration)."""
    return (
        int(sum_by_type(effects, EffectTypes.BaseVocalUp)),
        int(sum_by_type(effects, EffectTypes.BaseExpressionUp)),
        int(sum_by_type(effects, EffectTypes.BaseConcentrationUp)),
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
    for em, lv in effects:
        if int(em.type) != int(EffectTypes.PrincipalGaugeLimitUp):
            continue
        if int(em.fire_timing_type) != int(FireTimingTypes.Passive):
            continue
        v = _detail_value(em, lv)
        if int(em.calculation_type) == 3:  # FixedAddition
            flat += v
        elif int(em.calculation_type) == 1:  # PercentageAddition (/10000)
            pct += v
    return int(_BASE_MAX_PRINCIPAL * (1 + pct / 10000) + flat)


def base_correction(effects: list) -> float:
    """BaseCorrection (type 4, PercentageAddition, Self) -> percent points on the character base
    (the leaf's w5 term; value 200 = +2%). Bloom 'performance up' bonuses are BaseCorrection.
    """
    return sum_by_type(effects, EffectTypes.BaseCorrection) / 100.0


# Constants.Character: caps on the status/performance percent, raised by the matching *LimitUp.
_STATUS_PERCENT_LIMIT = 20000
_PERFORMANCE_PERCENT_LIMIT = 20000


def percent_bonus(effects: list) -> tuple:
    """Performance % applied to the base status (CalculatePartyStatus: status += base*pct/10000,
    denominator = Constants.Live.PercentAdditionDenominator = 10000). <Component>Up is per-component
    (capped at StatusPercentLimit + <Component>LimitUp), PerformanceUp applies to all three (capped at
    PerformancePercentLimit + PerformanceLimitUp). Returns (vocal, expression, concentration).
    """
    perf = min(
        sum_by_type(effects, EffectTypes.PerformanceUp),
        _PERFORMANCE_PERCENT_LIMIT
        + sum_by_type(effects, EffectTypes.PerformanceLimitUp),
    )

    def _comp(up, limit_up) -> float:
        return min(
            sum_by_type(effects, up),
            _STATUS_PERCENT_LIMIT + sum_by_type(effects, limit_up),
        )

    return (
        int(_comp(EffectTypes.VocalUp, EffectTypes.VocalLimitUp) + perf),
        int(_comp(EffectTypes.ExpressionUp, EffectTypes.ExpressionLimitUp) + perf),
        int(
            _comp(EffectTypes.ConcentrationUp, EffectTypes.ConcentrationLimitUp) + perf
        ),
    )


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
    """Extra lights granted to a sense by AddSenseLight* effects (incl. wildcards)."""
    lights: list = []
    for em, lv in effects:
        light = _light_of(int(em.type), sense_type)
        if light is not None:
            lights += [light] * max(0, int(_detail_value(em, lv)))
    return lights


def start_effects(effects: list, actor_id: int, start_order: int = 0) -> list:
    """Effects with FireTimingTypes.StartLive as LiveUnit.StartEffects Effect entities."""
    result: list = []
    order = start_order
    for em, lv in effects:
        if int(em.fire_timing_type) != int(FireTimingTypes.StartLive):
            continue
        order += 1
        value = _detail_value(em, lv)
        # range Self -> this actor; All -> every actor (target_actor_id=None)
        target = actor_id if int(em.range) == 1 else None
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
