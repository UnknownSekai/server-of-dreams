"""Live-finish result computation for Lives/FinishAndValidate.

- clear lamp: from is_cleared + the note judges (Fail / Clear / FC / AP).
- rate grade: AchievementRateExtensions.GetAchievementRateGrade thresholds (reversed from 0xa5f97d8).
- achievement rate: exact mirror of InputCollector.CalculateAchievementRate (0xb94cf38) --
  sum(count[t] * weight[t]) / sum(count[t]) over every judged note. Only GOOD/GREAT/PERFECT/
  PERFECT_STAR carry weight; MISS/BAD contribute 0 to the numerator but still count in the
  denominator, so misses drag the rate down. Max attainable is 101 (all PERFECT_STAR).
"""

from models.enums import AchievementRateGrades, ClearLamps, TimingTypes

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


def clear_lamp(is_cleared: bool, judges) -> int:
    """Fail (not cleared) / AllPerfect (no mis. no imperfect) / FullCombo (no misses) / Clear."""
    if not is_cleared:
        return int(ClearLamps.None_)
    counts = {int(j.timing): j.count for j in (judges or [])}
    broken = counts.get(int(TimingTypes.MISS), 0) + counts.get(int(TimingTypes.BAD), 0)
    imperfect = counts.get(int(TimingTypes.GOOD), 0) + counts.get(
        int(TimingTypes.GREAT), 0
    )
    if broken == 0 and imperfect == 0:
        return int(ClearLamps.AllPerfect)
    if broken == 0:
        return int(ClearLamps.FullCombo)
    return int(ClearLamps.Clear)


def achievement_rate(judges) -> float:
    total = sum(j.count for j in (judges or []))
    if total == 0:
        return 0.0
    weighted = sum(j.count * _RATE_WEIGHT.get(int(j.timing), 0.0) for j in judges)
    return weighted / total


def rate_grade(rate: float) -> int:
    if rate > _RATE_CAP:
        return int(AchievementRateGrades.None_)
    for threshold, grade in _GRADE_THRESHOLDS:
        if rate >= threshold:
            return int(grade)
    return int(AchievementRateGrades.None_)
