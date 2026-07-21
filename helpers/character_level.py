"""Character leveling: the exp curve, the level ceiling, and experience items.

``CharacterLevelMaster`` is a 1:1 mirror of ``PlayerRankMaster`` -- 300 rows each -- because a
character's level is bounded by the player's rank. The ceiling used here is the *player rank
cap* (``User.playerRankLimit``, 50 on a fresh account and raised through PlayerRankCapMaster),
never past the levels the curve has actually released: each ``CharacterLevelMaster`` row carries
a ``start_date`` and the top of the table unlocks in batches over time.

``Character.currentExperience`` is read as exp *within* the current level, so a level-up
subtracts that level's ``experience_to_level_up`` rather than resetting the bar to 0. That
matches the master column being named per-level, but no capture pins it down -- if the client
ever shows a wrong progress bar, this is the assumption to revisit.
"""

from datetime import datetime, timezone
from typing import Optional

from helpers.cache import cache
from models.master_data.CharacterExperienceItemMaster import (
    CharacterExperienceItemMaster,
)

_LEVELS: dict = {}
_EXP_ITEMS: dict = {}


def _levels() -> dict:
    if not _LEVELS:
        _LEVELS.update({r.level: r for r in cache.character_level_master})
    return _LEVELS


def started(start_date: str, at: datetime) -> bool:
    # an unparseable/missing date reads as "no restriction", as in helpers.shops.available
    try:
        start = datetime.fromisoformat(start_date)
    except (TypeError, ValueError):
        return True
    if start.tzinfo is None:
        start = start.replace(tzinfo=timezone.utc)
    return start <= at


def released_max_level(now: Optional[datetime] = None) -> int:
    """The highest level the curve has released. Levels 271-300 were still dated in the
    future at the last masterdata pull, so this is below the table's 300."""
    at = now or datetime.now(timezone.utc)
    return max(
        (r.level for r in cache.character_level_master if started(r.start_date, at)),
        default=1,
    )


def level_cap(user, now: Optional[datetime] = None) -> int:
    """A character's maximum level for this player: the player rank cap, clamped to the
    released curve."""
    return max(1, min(user.playerRankLimit, released_max_level(now)))


def experience_to_level_up(level: int) -> Optional[int]:
    """Exp needed to get from ``level`` to the next one, or None past the table."""
    row = _levels().get(level)
    return row.experience_to_level_up if row is not None else None


def experience_to_reach(level: int, current_experience: int, target: int) -> int:
    """Exp still needed to reach ``target`` from a character's current standing (0 if it is
    already there)."""
    total = 0
    for lv in range(max(1, level), target):
        need = experience_to_level_up(lv)
        if need is None:  # off the end of the curve -- nothing further is reachable
            break
        total += need
    return max(0, total - current_experience)


def apply_experience(
    level: int, current_experience: int, gained: int, cap: int
) -> tuple[int, int]:
    """Spend ``gained`` exp on a character. Returns its ``(level, currentExperience)``.

    The cap itself is reachable -- a character levels *to* the player rank cap, not to one
    below it. Exp past the cap is banked in ``currentExperience`` rather than dropped, so it
    turns into levels the moment the rank cap is raised: call this with ``gained=0`` after an
    uncap to cash the bank in.
    """
    level = max(1, level)
    experience = current_experience + gained
    while level < cap:
        need = experience_to_level_up(level)
        if need is None or experience < need:
            break
        experience -= need
        level += 1
    return level, experience


def experience_item(item_master_id: int) -> Optional[CharacterExperienceItemMaster]:
    """The exp-item master for an item id, or None if that item isn't an exp item."""
    if not _EXP_ITEMS:
        _EXP_ITEMS.update(
            {r.item_master_id: r for r in cache.character_experience_item_master}
        )
    return _EXP_ITEMS.get(item_master_id)


def experience_items() -> list[CharacterExperienceItemMaster]:
    """Every exp item, richest first -- the order a bulk level-up spends a pool in."""
    experience_item(0)  # prime the index
    return sorted(
        _EXP_ITEMS.values(), key=lambda r: r.acquirable_experience, reverse=True
    )


def spend_from_pool(stock: dict, needed: int) -> dict:
    """Pick the exp items to burn from ``stock`` ({itemMasterId: owned}) to cover ``needed``
    exp. Returns {itemMasterId: quantity}.

    Richest item first, in whole steps that fit under ``needed``, so the smaller
    denominations fill in the remainder and as little as possible is spent overshooting.
    Whatever gap is left after that is smaller than every item still in stock, so the
    cheapest of those closes it -- refusing to overshoot there is what would strand a
    character short of its cap, and the excess is banked rather than lost anyway. Only a
    genuinely empty pool leaves the character below the cap.
    """
    # TODO: CharacterExperienceItemMaster.acquirable_experience_bonus (value/1000 for each of
    # the three items) is unused -- what it multiplies is unobserved.
    if needed <= 0:
        return {}
    items = experience_items()
    left = dict(stock)
    spend: dict = {}
    for master in items:
        value = master.acquirable_experience
        owned = left.get(master.item_master_id, 0)
        if value <= 0 or owned <= 0 or needed < value:
            continue
        quantity = min(owned, needed // value)
        if quantity > 0:
            spend[master.item_master_id] = quantity
            left[master.item_master_id] = owned - quantity
            needed -= quantity * value
    if needed > 0:
        for master in reversed(items):  # cheapest first
            if left.get(master.item_master_id, 0) > 0:
                _id = master.item_master_id
                spend[_id] = spend.get(_id, 0) + 1
                break
    return spend
