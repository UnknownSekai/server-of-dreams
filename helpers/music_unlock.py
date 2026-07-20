"""Stella / Olivier chart unlocks, derived from the user's live clears + live records.

Everything except an actual purchase is *derived* from the user's `live` rows against the
current live_master data, so a rerate (a chart's difficulty level changing between versions)
is handled automatically the next time we recompute.

Stella release (music.stellaReleased):
- Clearing a song's Extra chart releases that song's Stella chart.
- Once >= 10 Olivier charts are cleared (CLEAR or better), every owned (possessed) song's
  Stella is released -- including songs granted afterwards.
- Sticky: once released it stays released.

Olivier release (music.olivierReleaseStatus, OlivierReleaseStatuses):
- Released (purchased) is sticky -- a rerate never revokes it.
- Otherwise a song's Olivier is Purchasable iff its CURRENT level is <= the highest Olivier
  level the user has cleared. So clearing an Olivier at level N makes every Olivier of level
  <= N purchasable at once (future grants included); a rerate above that level drops back.
- Otherwise, S-rank (or better) on the song's Stella chart makes its Olivier Challengeable.
- Otherwise None.
"""

from db.user import get_lives
from helpers.cache import cache
from models.enums import (
    AchievementRateGrades,
    ClearLamps,
    MusicDifficulties,
    OlivierReleaseStatuses,
)

OLIVIER_STELLA_THRESHOLD = 10

_BY_ID: dict = {}
_BY_MUSIC: dict = {}


def _build() -> None:
    if _BY_ID:
        return
    for m in cache.live_master:
        _BY_ID[m.id_] = m
        _BY_MUSIC.setdefault(m.music_master_id, {})[m.difficulty] = m


def _live_master(live_master_id: int):
    _build()
    return _BY_ID.get(live_master_id)


def _chart(music_master_id: int, difficulty: MusicDifficulties):
    _build()
    return _BY_MUSIC.get(music_master_id, {}).get(difficulty)


def _is_difficulty(live_master_id: int, difficulty: MusicDifficulties) -> bool:
    lm = _live_master(live_master_id)
    return lm is not None and lm.difficulty == difficulty


def _cleared(row) -> bool:
    return row.clearLamp >= int(ClearLamps.Clear)


_UNLOCK_DIFFICULTIES = (
    MusicDifficulties.Extra,
    MusicDifficulties.Stella,
    MusicDifficulties.Olivier,
)


def affects_unlocks(live_master_id: int) -> bool:
    """Whether finishing this chart could change any Stella/Olivier release state. Only Extra
    (stella), Stella (olivier challengeable) and Olivier (purchasable / 10-clear stella) can;
    Normal/Hard never do, so those finishes skip the whole re-derivation."""
    lm = _live_master(live_master_id)
    return lm is not None and lm.difficulty in _UNLOCK_DIFFICULTIES


def count_olivier_clears(lives) -> int:
    return sum(
        1
        for r in lives
        if _cleared(r) and _is_difficulty(r.liveMasterId, MusicDifficulties.Olivier)
    )


class MusicProgress:
    """Aggregates of a user's live records, used to resolve per-song unlock state."""

    def __init__(self, lives) -> None:
        self.all_stella = count_olivier_clears(lives) >= OLIVIER_STELLA_THRESHOLD
        self.max_cleared_olivier_level = 0
        self.extra_cleared: set[int] = set()
        self.stella_s_ranked: set[int] = set()
        for r in lives:
            lm = _live_master(r.liveMasterId)
            if lm is None:
                continue
            if lm.difficulty == MusicDifficulties.Olivier and _cleared(r):
                self.max_cleared_olivier_level = max(
                    self.max_cleared_olivier_level, lm.level
                )
            elif lm.difficulty == MusicDifficulties.Extra and _cleared(r):
                self.extra_cleared.add(lm.music_master_id)
            elif lm.difficulty == MusicDifficulties.Stella and r.rateGrade >= int(
                AchievementRateGrades.S
            ):
                self.stella_s_ranked.add(lm.music_master_id)

    def stella_released(
        self, music_master_id: int, is_possession: bool, stored: bool
    ) -> bool:
        if stored:
            return True  # sticky once released
        if self.all_stella and is_possession:
            return True
        return music_master_id in self.extra_cleared

    def olivier_status(self, music_master_id: int, stored: int) -> int:
        if stored == int(OlivierReleaseStatuses.Released):
            return int(
                OlivierReleaseStatuses.Released
            )  # purchased -> sticky across rerates
        olivier = _chart(music_master_id, MusicDifficulties.Olivier)
        if olivier is None:
            return int(OlivierReleaseStatuses.None_)
        if olivier.level <= self.max_cleared_olivier_level:
            return int(OlivierReleaseStatuses.Purchasable)
        if music_master_id in self.stella_s_ranked:
            return int(OlivierReleaseStatuses.Challengeable)
        return int(OlivierReleaseStatuses.None_)


async def load_progress(conn, user_id: int) -> MusicProgress:
    return MusicProgress(await conn.fetch(get_lives(user_id)))


async def granted_music_state(
    conn, user_id: int, music_master_id: int
) -> tuple[bool, int]:
    """(stellaReleased, olivierReleaseStatus) a freshly granted, possessed song starts at,
    given the user's current progress (so a song earned after the thresholds is born unlocked).
    """
    progress = await load_progress(conn, user_id)
    return (
        progress.stella_released(music_master_id, True, False),
        progress.olivier_status(music_master_id, int(OlivierReleaseStatuses.None_)),
    )
