"""What awakening, talent bloom and sense enhancement cost.

All three price a step off the character's ``CharacterMaster``:

- **awakening** -- ``character_awakening_item_group_master_id`` lists the items for the phase
  being left. Every group in the current masterdata describes only phase 0, so awakening is
  the single step 0 -> 1, and the 42 characters with no group can't awaken at all.
- **sense** -- ``sense_enhance_item_group_master_id`` lists the items for each level being
  left, so a multi-level jump is the sum of the steps it passes through.
- **bloom** -- ``CharacterBloomItemMaster`` keyed by (rarity, stage being left): a count of
  the character's own pieces, plus a flat item cost on the last stage of a 6-stage character.

Pieces have a generic stand-in the player may pay with instead -- ジュゴン像 for an ordinary
piece (at the piece's own ``dugong_required_amount`` exchange rate) and the character base's
万能ダイピース for a dai piece. The request carries no choice of payment, so :func:`bloom_cost`
decides: own pieces first, generic for whatever is missing.
"""

from datetime import datetime, timezone
from typing import Optional

from helpers.cache import cache
from helpers.character_level import started
from models.enums import TalentBloomItemTypes

_INDEX: dict = {}


def _by_id(table: str) -> dict:
    if table not in _INDEX:
        _INDEX[table] = {r.id_: r for r in getattr(cache, table)}
    return _INDEX[table]


def character_master(character_master_id: int):
    """The CharacterMaster row a character is built from, or None."""
    return _by_id("character_master").get(character_master_id)


def _add(cost: dict, item_master_id: int, quantity: int) -> None:
    cost[item_master_id] = cost.get(item_master_id, 0) + quantity


# --- awakening ---------------------------------------------------------------------------


def max_awakening_phase(master) -> int:
    """The phase an awakened character sits at (0 when it can't awaken)."""
    group = _by_id("character_awakening_item_group_master").get(
        master.character_awakening_item_group_master_id
    )
    if group is None or not group.items:
        return 0
    return max(i.awakening_phase for i in group.items) + 1


def awakening_cost(master, phase: int) -> Optional[dict]:
    """The items to awaken out of ``phase``, or None when there is no such step."""
    group = _by_id("character_awakening_item_group_master").get(
        master.character_awakening_item_group_master_id
    )
    if group is None:
        return None
    cost: dict = {}
    for item in group.items or []:
        if item.awakening_phase == phase:
            _add(cost, item.item_master_id, item.required_quantity)
    return cost or None


# --- sense enhancement -------------------------------------------------------------------


def max_sense_level(master) -> int:
    """The highest sense level this character's enhance group can reach."""
    group = _by_id("character_sense_enhance_item_group_master").get(
        master.sense_enhance_item_group_master_id
    )
    if group is None or not group.items:
        return 1
    return max(i.current_level for i in group.items) + 1


def sense_enhance_cost(master, level_from: int, level_to: int) -> Optional[dict]:
    """The items to take a sense from ``level_from`` to ``level_to``, or None if any step in
    between isn't priced."""
    group = _by_id("character_sense_enhance_item_group_master").get(
        master.sense_enhance_item_group_master_id
    )
    if group is None or level_to <= level_from:
        return None
    cost: dict = {}
    for level in range(level_from, level_to):
        step = [i for i in group.items or [] if i.current_level == level]
        if not step:
            return None
        for item in step:
            _add(cost, item.item_master_id, item.required_quantity)
    return cost


# --- talent bloom ------------------------------------------------------------------------


def max_talent_stage(master, now: Optional[datetime] = None) -> int:
    """The highest bloom stage available. ``max_talent_stage_release_date`` dates the final
    stage -- characters carrying one all bloom to 6, the ones without stop at 5 -- so a date
    that hasn't arrived holds the character one stage short."""
    if master.max_talent_stage_release_date and not started(
        master.max_talent_stage_release_date, now or datetime.now(timezone.utc)
    ):
        return max(0, master.max_talent_stage - 1)
    return master.max_talent_stage


def _bloom_step(rarity: int, stage: int):
    for row in cache.character_bloom_item_master:
        if int(row.rarity) == int(rarity) and row.current_stage == stage:
            return row
    return None


def _piece(character_master_id: int, bloom_item_type):
    for row in cache.character_piece_master:
        if row.character_master_id == character_master_id and int(
            row.talent_bloom_item_type
        ) == int(bloom_item_type):
            return row
    return None


def _generic_piece(master, step, piece) -> tuple[Optional[int], int]:
    """The stand-in item for a step's piece, and how many of it one piece is worth."""
    if int(step.talent_bloom_item_type) == int(TalentBloomItemTypes.ActorDaiPiece):
        # dai pieces are covered by the character base's 万能ダイピース, one for one
        for row in cache.character_base_bloom_generic_item_master:
            if row.character_base_master_id == master.character_base_master_id and int(
                row.talent_bloom_item_type
            ) == int(step.talent_bloom_item_type):
                return row.item_master_id, 1
        return None, 0
    return step.generic_bloom_item_master_id, piece.dugong_required_amount


def bloom_cost(master, stage_from: int, stage_to: int, stock: dict) -> Optional[dict]:
    """The items a bloom from ``stage_from`` to ``stage_to`` costs the player, or None when a
    step isn't priced or can't be paid for at all.

    ``stock`` ({itemMasterId: owned}) is read, never written. It is needed because the payment
    isn't fixed: the character's own pieces go first and the generic stand-in covers the
    shortfall, so what the player owns decides the bill.
    """
    remaining = dict(stock)
    cost: dict = {}
    for stage in range(stage_from, stage_to):
        step = _bloom_step(master.rarity, stage)
        piece = _piece(master.id_, step.talent_bloom_item_type) if step else None
        if step is None or piece is None:
            return None

        own = min(step.required_piece_amount, remaining.get(piece.item_master_id, 0))
        if own:
            remaining[piece.item_master_id] -= own
            _add(cost, piece.item_master_id, own)
        short = step.required_piece_amount - own
        if short:
            generic, rate = _generic_piece(master, step, piece)
            if generic is None or rate <= 0 or master.forbid_generic_item_bloom:
                return None
            if remaining.get(generic, 0) < short * rate:
                return None
            remaining[generic] -= short * rate
            _add(cost, generic, short * rate)

        if step.required_item_master_id and step.required_item_amount:
            if (
                remaining.get(step.required_item_master_id, 0)
                < step.required_item_amount
            ):
                return None
            remaining[step.required_item_master_id] -= step.required_item_amount
            _add(cost, step.required_item_master_id, step.required_item_amount)
    return cost or None


def bloom_rewards(master, stage_from: int, stage_to: int) -> list:
    """The ``(thing_type, thing_id, quantity)`` handed out for the stages newly reached."""
    group = _by_id("character_bloom_bonus_group_master").get(
        master.bloom_bonus_group_master_id
    )
    if group is None:
        return []
    return [
        (int(r.thing_type), r.thing_id, r.thing_quantity)
        for r in group.bloom_rewards or []
        if stage_from < r.phase <= stage_to
    ]
