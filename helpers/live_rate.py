"""Live rate (the per-chart / player rating for Stella-or-lower charts).

A chart's live rate = its level + an achievement-based adjustment. Charts with no live rate:
Olivier (an Olivier play only updates achievement_rate_result, the raw
best %, never the live rating) and any chart of a long-version song (MusicMaster.is_long_version).
For those, live_rate_result is 0/0 (best_ever and this_time) and the total rate is unchanged
regardless of the result. The player's total rate is the sum of the best live rate of their
top 30 charts.

Achievement-rate -> adjustment breakpoints (>= threshold wins):
  101.00% +6.05 | 100.95% +6.00 | 100.75% +4.50 | 100.50% +3.00 | 100.25% +2.25
  100.00% +1.50 |  99.00% +0.75 |  98.00% +0.00 |  97.50% -1.00
Below 97.50% falls to the lowest bracket (-1.00) -- lower brackets aren't published.
"""

from typing import Optional

from helpers.cache import cache
from models.enums import MusicDifficulties

_TOP_N = 30
_ADJUSTMENTS = (
    (101.00, 6.05),
    (100.95, 6.00),
    (100.75, 4.50),
    (100.50, 3.00),
    (100.25, 2.25),
    (100.00, 1.50),
    (99.00, 0.75),
    (98.00, 0.00),
    (97.50, -1.00),
)

_BY_ID: dict = {}
_MUSIC: dict = {}


def _build() -> None:
    if not _BY_ID:
        _BY_ID.update({m.id_: m for m in cache.live_master})
        _MUSIC.update({m.id_: m for m in cache.music_master})


def _rated_chart(live_master_id: int):
    """The chart if it participates in live rate -- Stella-or-lower difficulty and not a
    long-version song -- else None."""
    _build()
    lm = _BY_ID.get(live_master_id)
    if lm is None or int(lm.difficulty) > int(MusicDifficulties.Stella):
        return None
    music = _MUSIC.get(lm.music_master_id)
    if music is not None and music.is_long_version:
        return None
    return lm


def _adjustment(rate: float) -> float:
    for threshold, adj in _ADJUSTMENTS:
        if rate >= threshold:
            return adj
    return _ADJUSTMENTS[-1][1]


def live_rate(level: int, rate: float) -> float:
    return round(level + _adjustment(rate), 2)


def chart_live_rate(live_master_id: int, rate: float) -> Optional[float]:
    """A chart's live rate, or None if it has none (Olivier / long-version / unknown chart)."""
    lm = _rated_chart(live_master_id)
    return None if lm is None else live_rate(lm.level, rate)


def total_rate(pairs) -> float:
    """Sum of the top 30 chart live rates. ``pairs`` = iterable of (live_master_id, rate)."""
    rates = sorted(
        (
            r
            for r in (chart_live_rate(mid, rate) for mid, rate in pairs)
            if r is not None
        ),
        reverse=True,
    )
    return round(sum(rates[:_TOP_N]), 2)


def chart_live_rate_result(
    live_master_id: int, this_rate: float, prev_rate: float
) -> tuple[float, float]:
    """(best_ever, this_time) live rate for the finished chart. A chart with no live rate
    (Olivier / long-version) is (0.0, 0.0). ``best_ever`` is the PAST best only (excludes this
    play) -- 0 when never played before."""
    lm = _rated_chart(live_master_id)
    if lm is None:
        return 0.0, 0.0
    best_ever = live_rate(lm.level, prev_rate) if prev_rate > 0 else 0.0
    return best_ever, live_rate(lm.level, this_rate)
