import unittest
from unittest.mock import MagicMock

from helpers.effects import (
    AppliedEffect,
    EffectSourceTypes,
    base_stat_bonus,
    collect_slot_effects,
    component_flat_bonus,
    component_percent_bonuses_by_source,
    leader_sense_effects,
    performance_percent_bonuses_by_source,
)
from helpers.live import (
    _calculate_slot_status,
    _character_base_status,
)
from models.entities import LiveStatus
from models.enums import EffectTypes


class TestStatusCalculation(unittest.TestCase):
    def test_character_base_status(self):
        # Mock CharacterMaster with min_level_status: Vocal=53, Expr=66, Conc=61
        cm = MagicMock()
        cm.min_level_status.vocal = 53
        cm.min_level_status.expression = 66
        cm.min_level_status.concentration = 61

        # Level 300 (status_level = 15084 -> 150.84), Awakening 1 (+10%), Side story = 5
        # Base: (53+5)=58, (66+5)=71, (61+5)=66
        # Formula: floor(base * sl * factor)
        # Vocal: floor(58 * 150.84 * 1.10) = floor(9623.592) = 9623
        # Expr: floor(71 * 150.84 * 1.10) = floor(11780.604) = 11780
        # Conc: floor(66 * 150.84 * 1.10) = floor(10950.984) = 10950
        from helpers import live

        orig_status_level = live._status_level
        try:
            live._status_level = lambda lvl: 15084 if lvl == 300 else 10000
            v, e, c = _character_base_status(
                cm,
                level=300,
                base_stat_bonuses=(0, 0, 0),
                story_read_bonus=5,
                intrinsic=10.0,
            )
            self.assertEqual(v, 9623)
            self.assertEqual(e, 11780)
            self.assertEqual(c, 10950)
        finally:
            live._status_level = orig_status_level

    def test_slot_status_all_five_slots(self):
        # Verification test cases covering 5 standard party slots
        slots_data = [
            (
                "Slot 1 (Kokona)",
                (9623, 11780, 10950),
                (1500, 0, 0),  # Album +700, Acc +800 Vocal
                {
                    int(EffectSourceTypes.Other): (600, 600, 600)
                },  # Circle +6% to all stats
                {
                    int(EffectSourceTypes.Album): 4500,  # Album +45%
                    int(EffectSourceTypes.Poster): 15500,  # Poster +155%
                },
                (35100, 37457, 34820, 107377),
            ),
            (
                "Slot 2 (Kathrina)",
                (11448, 10785, 10121),
                (0, 800, 0),  # Acc +800 Expr
                {int(EffectSourceTypes.Other): (600, 600, 600)},
                {
                    int(EffectSourceTypes.Album): 4500,
                    int(EffectSourceTypes.Poster): 15500,
                },
                (36401, 36695, 32183, 105279),
            ),
            (
                "Slot 3 (Yae)",
                (10287, 10950, 11116),
                (0, 0, 800),  # Acc +800 Conc
                {int(EffectSourceTypes.Other): (600, 600, 600)},
                {
                    int(EffectSourceTypes.Album): 4500,
                    int(EffectSourceTypes.Poster): 15500,
                },
                (32711, 34820, 37745, 105276),
            ),
            (
                "Slot 4 (Panda)",
                (10453, 10950, 10950),
                (0, 0, 0),
                {
                    int(EffectSourceTypes.Poster): (6600, 0, 0),  # Poster +66% Vocal
                    int(EffectSourceTypes.Other): (600, 600, 600),
                },
                {
                    int(EffectSourceTypes.Album): 4500,
                    int(EffectSourceTypes.Poster): 13000,
                    int(EffectSourceTypes.Accessory): 2500,
                },
                (53933, 34820, 34820, 123573),
            ),
            (
                "Slot 5 (Shizuka)",
                (10950, 10287, 11116),
                (0, 0, 0),
                {int(EffectSourceTypes.Other): (600, 600, 600)},
                {
                    int(EffectSourceTypes.Album): 4500,
                    int(EffectSourceTypes.Poster): 15500,
                },
                (34820, 32711, 35345, 102876),
            ),
        ]

        total_party_status = 0
        for name, base, flat, comp_pcts, perf_pcts, expected in slots_data:
            st = _calculate_slot_status(
                base,
                flat,
                comp_pcts,
                perf_pcts,
            )
            exp_v, exp_e, exp_c, exp_tot = expected
            self.assertEqual(st.vocal, exp_v, f"Vocal mismatch in {name}")
            self.assertEqual(st.expression, exp_e, f"Expression mismatch in {name}")
            self.assertEqual(
                st.concentration, exp_c, f"Concentration mismatch in {name}"
            )
            self.assertEqual(st.total_status, exp_tot, f"Total mismatch in {name}")
            total_party_status += st.total_status

        self.assertEqual(total_party_status, 544381)

    def test_effect_extraction_helpers(self):
        # Create mock effect master objects
        def make_eff(eff_type, calc_type, val, range_val=1):
            em = MagicMock()
            em.type = eff_type
            em.calculation_type = calc_type
            em.range = range_val
            detail = MagicMock()
            detail.level = 1
            detail.value = val
            em.details = [detail]
            return em

        effects = [
            AppliedEffect(
                make_eff(EffectTypes.BaseVocalUp, 3, 50), 1, EffectSourceTypes.Other
            ),
            AppliedEffect(
                make_eff(EffectTypes.BaseExpressionUp, 3, 40),
                1,
                EffectSourceTypes.Other,
            ),
            AppliedEffect(
                make_eff(EffectTypes.BaseConcentrationUp, 3, 30),
                1,
                EffectSourceTypes.Other,
            ),
            AppliedEffect(
                make_eff(EffectTypes.VocalUp, 3, 400), 1, EffectSourceTypes.Accessory
            ),
            AppliedEffect(
                make_eff(EffectTypes.ExpressionUp, 3, 300),
                1,
                EffectSourceTypes.Accessory,
            ),
            AppliedEffect(
                make_eff(EffectTypes.ConcentrationUp, 3, 200),
                1,
                EffectSourceTypes.Accessory,
            ),
            AppliedEffect(
                make_eff(EffectTypes.VocalUp, 1, 1500), 1, EffectSourceTypes.Poster
            ),
            AppliedEffect(
                make_eff(EffectTypes.PerformanceUp, 1, 2500), 1, EffectSourceTypes.Album
            ),
            AppliedEffect(
                make_eff(EffectTypes.PerformanceUp, 1, 5000),
                1,
                EffectSourceTypes.Poster,
            ),
        ]

        # Base stat bonus (type 3)
        self.assertEqual(base_stat_bonus(effects), (50, 40, 30))

        # Component flat bonus (type 3)
        self.assertEqual(component_flat_bonus(effects), (400, 300, 200))

        # Component percent by source (type 1)
        comp_pcts = component_percent_bonuses_by_source(effects)
        self.assertIn(int(EffectSourceTypes.Poster), comp_pcts)
        self.assertEqual(comp_pcts[int(EffectSourceTypes.Poster)], (1500, 0, 0))

        # Performance percent by source (type 1)
        perf_pcts = performance_percent_bonuses_by_source(effects)
        self.assertEqual(perf_pcts[int(EffectSourceTypes.Album)], 2500)
        self.assertEqual(perf_pcts[int(EffectSourceTypes.Poster)], 5000)

    def test_capping_order_by_source_priority(self):
        # When limits are reached, earlier sources in priority order get allocated first
        def make_eff(eff_type, calc_type, val):
            em = MagicMock()
            em.type = eff_type
            em.calculation_type = calc_type
            detail = MagicMock()
            detail.level = 1
            detail.value = val
            em.details = [detail]
            return em

        # Normal cap is 20000 (200%). If Album has 15000 and Poster has 10000,
        # Album should get 15000 and Poster should be capped to 5000 (remaining cap).
        effects = [
            AppliedEffect(
                make_eff(EffectTypes.PerformanceUp, 1, 15000),
                1,
                EffectSourceTypes.Album,
            ),
            AppliedEffect(
                make_eff(EffectTypes.PerformanceUp, 1, 10000),
                1,
                EffectSourceTypes.Poster,
            ),
        ]
        perf_pcts = performance_percent_bonuses_by_source(effects)
        self.assertEqual(perf_pcts[int(EffectSourceTypes.Album)], 15000)
        self.assertEqual(perf_pcts[int(EffectSourceTypes.Poster)], 5000)

    def test_accessory_fixed_effects(self):
        from helpers import effects

        # Mock accessory effect & effect master
        em_fixed = MagicMock()
        em_fixed.id_ = 1001
        em_fixed.type = EffectTypes.PerformanceUp
        em_fixed.conditions = []

        em_rand = MagicMock()
        em_rand.id_ = 1002
        em_rand.type = EffectTypes.VocalUp
        em_rand.conditions = []

        aem_fixed = MagicMock()
        aem_fixed.id_ = 501
        aem_fixed.effect_master_id = 1001

        aem_rand = MagicMock()
        aem_rand.id_ = 502
        aem_rand.effect_master_id = 1002

        am = MagicMock()
        am.id_ = 301
        am.fixed_accessory_effects = [501]

        acc = MagicMock()
        acc.accessoryMasterId = 301
        acc.level = 10
        acc.accessoryEffects = [502]

        orig_aem = effects._aem
        orig_em = effects._em
        orig_am = effects._am
        try:
            effects._aem = lambda aid: (
                aem_fixed if aid == 501 else (aem_rand if aid == 502 else None)
            )
            effects._em = lambda eid: (
                em_fixed if eid == 1001 else (em_rand if eid == 1002 else None)
            )
            effects._am = lambda mid: am if mid == 301 else None

            collected = collect_slot_effects(
                sense_master=None,
                star_act_master=None,
                sense_level=1,
                accessory=acc,
                poster=None,
                comp=None,
            )
            # Both fixed (1001) and random (1002) should be collected
            self.assertEqual(len(collected), 2)
            self.assertEqual(collected[0][0].id_, 1001)
            self.assertEqual(collected[0][1], 10)
            self.assertEqual(collected[0][2], EffectSourceTypes.Accessory)
            self.assertEqual(collected[1][0].id_, 1002)
            self.assertEqual(collected[1][1], 10)
            self.assertEqual(collected[1][2], EffectSourceTypes.Accessory)
        finally:
            effects._aem = orig_aem
            effects._em = orig_em
            effects._am = orig_am

    def test_leader_sense_effects(self):
        from helpers import effects

        leader_cm = MagicMock()
        leader_cm.leader_sense_master_id = 123

        matching_member = MagicMock()
        cat_match = MagicMock()
        cat_match.category_master_id = 8007
        matching_member.categories = [cat_match]

        non_matching_member = MagicMock()
        cat_non = MagicMock()
        cat_non.category_master_id = 1001
        non_matching_member.categories = [cat_non]

        lsm = MagicMock()
        lsm.id_ = 123
        detail = MagicMock()
        detail.effect_master_id = 9999
        cond = MagicMock()
        cond.category_master_id1 = 8007
        cond.category_master_id2 = None
        cond.category_master_id3 = None
        cond.category_master_id4 = None
        cond.category_master_id5 = None
        detail.conditions = [cond]
        lsm.details = [detail]

        em = MagicMock()
        em.id_ = 9999

        orig_lsm = effects._lsm
        orig_em = effects._em
        try:
            effects._lsm = lambda lid: lsm if lid == 123 else None
            effects._em = lambda eid: em if eid == 9999 else None

            effs_match = leader_sense_effects(leader_cm, matching_member)
            self.assertEqual(len(effs_match), 1)
            self.assertEqual(effs_match[0][0].id_, 9999)
            self.assertEqual(effs_match[0][1], 1)
            self.assertEqual(effs_match[0][2], EffectSourceTypes.LeaderSense)

            effs_non = leader_sense_effects(leader_cm, non_matching_member)
            self.assertEqual(len(effs_non), 0)
        finally:
            effects._lsm = orig_lsm
            effects._em = orig_em

    def test_final_performance_multiplier(self):
        from helpers.effects import final_performance_multiplier
        from models.enums import CalculationTypes, EffectTypes

        em = MagicMock()
        em.type = EffectTypes.FinalPerformanceUpCancelSense
        em.calculation_type = CalculationTypes.Multiplication
        detail = MagicMock()
        detail.level = 14
        detail.value = 200.0  # 200% -> 2.0x
        em.details = [detail]

        effs = [AppliedEffect(em, 14, EffectSourceTypes.Poster)]
        mult = final_performance_multiplier(effs)
        self.assertEqual(mult, 2.0)

        # Verify _calculate_slot_status with multiplier
        status = _calculate_slot_status(
            char_status=(10000, 10000, 10000),
            flat_bonuses=(0, 0, 0),
            comp_pcts={},
            perf_pcts={},
            multiplier=mult,
        )
        self.assertEqual(status.vocal, 20000)
        self.assertEqual(status.expression, 20000)
        self.assertEqual(status.concentration, 20000)
        self.assertEqual(status.total_status, 60000)

    def test_opening_star_act_and_reductions(self):
        from helpers.effects import decrease_require_lights, start_lights
        from helpers.live import _live_time_event, _star_act_condition
        from models.enums import FireTimingTypes, SenseLightTypes

        # Mock light decrease effect (e.g. DecreaseRequireAmplificationLight -1)
        em_dec = MagicMock()
        em_dec.type = EffectTypes.DecreaseRequireAmplificationLight
        detail_dec = MagicMock()
        detail_dec.level = 1
        detail_dec.value = 1.0
        em_dec.details = [detail_dec]

        reductions = decrease_require_lights(
            [AppliedEffect(em_dec, 1, EffectSourceTypes.BloomBonus)]
        )
        self.assertEqual(reductions.get(SenseLightTypes.Amplification), 1)

        # Mock start lights (FireTimingTypes.StartLive)
        em_light = MagicMock()
        em_light.fire_timing_type = FireTimingTypes.StartLive
        em_light.type = EffectTypes.AddSenseLightAmplification
        detail_light = MagicMock()
        detail_light.level = 1
        detail_light.value = 2.0
        em_light.details = [detail_light]

        lights = start_lights(
            [AppliedEffect(em_light, 1, EffectSourceTypes.Poster)], sense_type=0
        )
        self.assertEqual(
            lights, [SenseLightTypes.Amplification, SenseLightTypes.Amplification]
        )

        # Test _live_time_event with opening star act condition
        # Condition: Amplification=2, Support=1, Free=0
        req = {SenseLightTypes.Amplification: 2, SenseLightTypes.Support: 1}
        # Initial lights: [Amplification, Amplification, Support]
        init_lights = [
            SenseLightTypes.Amplification,
            SenseLightTypes.Amplification,
            SenseLightTypes.Support,
        ]
        pos_sense = {}
        lte = _live_time_event(
            pos_sense=pos_sense,
            music_time_second=100,
            sense_notation=None,
            star_act_condition=(req, 0),
            initial_lights=init_lights,
        )
        # Event at timing 0 should be opening star act
        self.assertGreater(len(lte.timings), 0)
        t0 = lte.timings[0]
        self.assertEqual(t0.timing_seconds, 0)
        self.assertTrue(t0.event.is_star_act)
        self.assertEqual(t0.event.grant_sense_lights, init_lights)
        self.assertEqual(t0.event.acquirable_lights, init_lights)


if __name__ == "__main__":
    unittest.main()
