"""Stamina: currentStamina + maxStaminaRestoredAt (the "full at" time). Effective stamina
is recomputed from that timestamp, so the value passively recovers 1 per
``stamina_recovery_seconds`` up to PlayerRankMaster.max_stamina for the player's rank.

Mirrors sekai-api-emulator's boost system: all mutation goes through the atomic
``adjust_user_stamina_atomic`` query so concurrent requests can't corrupt the count.
"""

import math
import time
from typing import Optional

from db.user import adjust_user_stamina_atomic
from helpers.cache import cache
from helpers.config import config

_MICRO = 1_000_000


def recovery_micros() -> int:
    return int(config["stamina_recovery_seconds"]) * _MICRO


def max_stamina(player_rank: int) -> int:
    """Max stamina for a player rank, from PlayerRankMaster (0 if the rank is unknown)."""
    for row in cache.player_rank_master:
        if row.rank == player_rank:
            return row.max_stamina
    return 0


def effective_stamina(current: int, restored_at: int, max_st: int, now: int) -> int:
    """Stamina right now, accounting for passive recovery. Overfilled stamina (above max,
    from items) never regenerates and is returned as-is."""
    if current >= max_st:
        return current
    interval = recovery_micros()
    if interval <= 0 or now >= restored_at:
        return max_st
    missing = math.ceil((restored_at - now) / interval)
    return max(0, max_st - missing)


def restored_at(current: int, max_st: int, now: int) -> int:
    """The epoch-micros ``maxStaminaRestoredAt`` for a given current stamina (``now`` if
    already at/above max)."""
    if current >= max_st:
        return now
    return now + (max_st - current) * recovery_micros()


async def adjust_and_check_stamina(
    conn,
    user_id: int,
    delta: int,
    player_rank: int,
    now: Optional[int] = None,
    auto_max_clamp: bool = False,
) -> bool:
    """Recover-then-apply ``delta`` stamina atomically. Returns True on success, False if it
    would go below 0 (or exceed max in strict mode). Pass delta<0 to consume, >0 to recover.
    """
    if now is None:
        now = int(time.time() * _MICRO)
    row = await conn.fetchrow(
        adjust_user_stamina_atomic(
            user_id,
            delta,
            max_stamina(player_rank),
            recovery_micros(),
            now,
            auto_max_clamp,
        )
    )
    return row is not None
