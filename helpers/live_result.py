"""Live-finish result computation for Lives/FinishAndValidate.

Everything here is derived from payload.base_score_blocks, one block per judged note. The
client sends judges=null (and score/max_combo/is_cleared as 0/0/false), so the note judges
are only recoverable as the timing_type spread across those blocks.

- clear lamp: from is_cleared + the block timings (Fail / Clear / FC / AP).
- rate grade: AchievementRateExtensions.GetAchievementRateGrade thresholds (reversed from 0xa5f97d8).
- achievement rate: exact mirror of InputCollector.CalculateAchievementRate (0xb94cf38) --
  sum(weight[timing]) / note count. Only GOOD/GREAT/PERFECT/PERFECT_STAR carry weight;
  MISS/BAD contribute 0 to the numerator but still count in the denominator, so misses drag
  the rate down. Max attainable is 101 (all PERFECT_STAR).
"""

from models.enums import AchievementRateGrades, ClearLamps, TimingTypes
from models import BaseScoreBlock, FinishLivePayload

_RATE_WEIGHT = {
    int(TimingTypes.GOOD): 50.0,
    int(TimingTypes.GREAT): 80.0,
    int(TimingTypes.PERFECT): 100.0,
    int(TimingTypes.PERFECT_STAR): 101.0,
}

# GetAchievementRateGrade(rate) thresholds (%), highest first (reversed from 0xa5f97d8).
# Rate is capped at 101 in the binary; anything above returns None (unreachable in practice).
_RATE_CAP = 101.0
_GRADE_THRESHOLDS = (
    (100.95, AchievementRateGrades.SSS),
    (100.75, AchievementRateGrades.SSPlus),
    (100.5, AchievementRateGrades.SS),
    (100.25, AchievementRateGrades.SPlus),
    (100.0, AchievementRateGrades.S),
    (98.0, AchievementRateGrades.APlus),
    (95.0, AchievementRateGrades.A),
    (90.0, AchievementRateGrades.B),
    (80.0, AchievementRateGrades.C),
)


_BROKEN = (int(TimingTypes.MISS), int(TimingTypes.BAD))
_IMPERFECT = (int(TimingTypes.GOOD), int(TimingTypes.GREAT))


def clear_lamp(is_cleared: bool, base_score_blocks: list[BaseScoreBlock]) -> int:
    """Fail (not cleared) / AllPerfect (no mis. no imperfect) / FullCombo (no misses) / Clear."""
    if not is_cleared:
        return int(ClearLamps.None_)
    timings = [int(b.timing_type) for b in (base_score_blocks or [])]
    broken = sum(1 for t in timings if t in _BROKEN)
    imperfect = sum(1 for t in timings if t in _IMPERFECT)
    if broken == 0 and imperfect == 0:
        return int(ClearLamps.AllPerfect)
    if broken == 0:
        return int(ClearLamps.FullCombo)
    return int(ClearLamps.Clear)


def achievement_rate(base_score_blocks: list[BaseScoreBlock]) -> float:
    blocks = base_score_blocks or []
    total = len(blocks)
    if total == 0:
        return 0.0
    weighted = sum(_RATE_WEIGHT.get(int(b.timing_type), 0.0) for b in blocks)
    return weighted / total


def play_totals(payload: FinishLivePayload) -> tuple[int, bool]:
    """(score, is_cleared), derived from the hash-verified score blocks.

    The client submits score=0, max_combo=0, is_cleared=false and judges=null on
    FinishAndValidate -- it reports only the block lists, so every headline figure is the
    server's to recompute. Score is the sum of every block's score across all four lists;
    a run whose life never reached 0 is a clear.
    """
    lists = (
        payload.base_score_blocks,
        payload.sense_score_blocks,
        payload.star_act_score_blocks,
        payload.multi_live_additional_score_blocks,
    )
    score = sum(int(b.score) for lst in lists for b in (lst or []))
    base = payload.base_score_blocks or []
    is_cleared = bool(base) and int(base[-1].life) > 0
    return score, is_cleared


def rate_grade(rate: float) -> int:
    if rate > _RATE_CAP:
        return int(AchievementRateGrades.None_)
    for threshold, grade in _GRADE_THRESHOLDS:
        if rate >= threshold:
            return int(grade)
    return int(AchievementRateGrades.None_)
