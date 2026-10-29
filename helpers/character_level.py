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

The curve is not paid in full: ``RequiredExperienceCoefficient`` scales it by the character's
rarity (0.3 / 0.5 / 0.8 / 1.0). Both the requirement and the exp a character banks are in that
scaled unit, so ``experience_to_reach`` and ``apply_experience`` scale consistently -- see
``scaled_experience``.
"""

import math
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

from helpers.cache import cache
from models.enums import CharacterRarities
from models.master_data.CharacterExperienceItemMaster import (
    CharacterExperienceItemMaster,
)

_LEVELS: dict = {}
_EXP_ITEMS: dict = {}
_CHARACTERS: dict = {}

# How much of the curve a character actually has to pay, by rarity. Recovered from the client:
# `Constants.Character.RequiredExperienceCoefficient` is filled in its `.cctor` with
# `Decimal..ctor(lo, mid, hi, isNegative, scale)` arguments 3/5/8/10 at scale 1, i.e. these
# decimals -- reading the lo word alone (3/5/8/10) gives values ten times too large.
# The client multiplies the *summed* curve by this (`CharacterEnhanceLevelUpModel
# .GetLimitLevelTotalExp` returns the raw total, `CalculationConsumeExpItem` scales it), so the
# coefficient is applied to a cumulative figure here too, never per level.
_REQUIRED_EXPERIENCE_COEFFICIENT: dict = {
    CharacterRarities.Rare1: Decimal("0.3"),
    CharacterRarities.Rare2: Decimal("0.5"),
    CharacterRarities.Rare3: Decimal("0.8"),
    CharacterRarities.Rare4: Decimal("1.0"),
}
_MAX_EXPERIENCE_COEFFICIENT = Decimal("1.0")
# the client's `fcsel` yields 0 for a rarity it does not recognise
_UNKNOWN_RARITY_COEFFICIENT = Decimal(0)


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


def _characters() -> dict:
    if not _CHARACTERS:
        _CHARACTERS.update({r.id_: r for r in cache.character_master})
    return _CHARACTERS


def character_rarity(character_master_id: int) -> Optional[CharacterRarities]:
    """The rarity of the character a master id refers to, or None if it is unknown."""
    master = _characters().get(character_master_id)
    return getattr(master, "rarity", None) if master is not None else None


def required_experience_coefficient(rarity: Optional[CharacterRarities]) -> Decimal:
    """The fraction of the raw curve a character of ``rarity`` pays.

    A rarity the client has no entry for scales by 0, matching its lookup fallback rather than
    guessing a default.
    """
    if rarity is None:
        return _UNKNOWN_RARITY_COEFFICIENT
    return _REQUIRED_EXPERIENCE_COEFFICIENT.get(rarity, _UNKNOWN_RARITY_COEFFICIENT)


def scaled_experience(amount: int, rarity: Optional[CharacterRarities]) -> int:
    """Apply the rarity coefficient to a raw exp amount, the way the client does.

    The client scales cumulative figures with ``decimal`` and truncates back to a whole number,
    so this keeps the same precision instead of using binary floats -- 0.3 and 0.8 are not
    exactly representable as floats and would drift on large totals.
    """
    if amount <= 0:
        return 0
    scaled = Decimal(amount) * required_experience_coefficient(rarity)
    # the coefficient never grows an amount, and a truncated value must not read as a level up
    return max(0, int(scaled))


def experience_to_reach(
    level: int,
    current_experience: int,
    target: int,
    rarity: Optional[CharacterRarities] = None,
) -> int:
    """Exp still needed to reach ``target`` from a character's current standing (0 if it is
    already there), scaled by ``rarity``.

    ``current_experience`` is stored against the *scaled* curve, so the whole requirement is
    scaled before subtracting it -- scaling the remainder instead would compare two different
    units.
    """
    total = 0
    for lv in range(max(1, level), target):
        need = experience_to_level_up(lv)
        if need is None:  # off the end of the curve -- nothing further is reachable
            break
        total += need
    return max(0, scaled_experience(total, rarity) - current_experience)


def apply_experience(
    level: int,
    current_experience: int,
    gained: int,
    cap: int,
    rarity: Optional[CharacterRarities] = None,
) -> tuple[int, int]:
    """Spend ``gained`` exp on a character. Returns its ``(level, currentExperience)``.

    Each level's requirement is scaled by ``rarity``, because a character's stored experience
    and its requirement have to be in the same unit: a rarity 1 character banks 0.3 of the raw
    curve per level, so it levels up against that same 0.3.

    The cap itself is reachable -- a character levels *to* the player rank cap, not to one
    below it. Exp past the cap is banked in ``currentExperience`` rather than dropped, so it
    turns into levels the moment the rank cap is raised: call this with ``gained=0`` after an
    uncap to cash the bank in.
    """
    level = max(1, level)
    experience = current_experience + gained
    while level < cap:
        need = experience_to_level_up(level)
        if need is None:
            break
        need = scaled_experience(need, rarity)
        if need <= 0 or experience < need:
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


def spend_from_pool(stock: dict, needed: int, bonus: float = 0) -> dict:
    """Pick the exp items to burn from ``stock`` ({itemMasterId: owned}) to cover ``needed``
    exp. Returns {itemMasterId: quantity}.

    Richest item first, in whole steps that fit under ``needed``, so the smaller
    denominations fill in the remainder and as little as possible is spent overshooting.
    Whatever gap is left after that is smaller than every item still in stock, so the
    cheapest of those closes it -- refusing to overshoot there is what would strand a
    character short of its cap, and the excess is banked rather than lost anyway. Only a
    genuinely empty pool leaves the character below the cap.

    ``bonus`` is the account's ``UserBonus.experienceBonus``; each item is priced at the
    same rounded effective exp that ``AddExperience`` grants, so the two level-up paths
    spend the same resources for the same result.
    """
    # The item's own ``acquirable_experience_bonus`` is added to the account's
    # experienceBonus by the level-up routes; it is not part of the item's price.
    if needed <= 0:
        return {}
    items = experience_items()
    left = dict(stock)
    spend: dict = {}
    for master in items:
        value = math.floor(master.acquirable_experience * (1 + bonus / 100))
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
