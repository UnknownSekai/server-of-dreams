"""Gacha lineup / roll-limit computation.

The per-rarity rates are NOT in the master data -- they are server-side config. Everything
else is derived from GachaMaster:

- a banner's pool is ``GachaMaster.things``; each thing's rarity comes from the
  Character/Poster master row it points at.
- ``pickup_order`` marks a pickup. Pickups take a flat per-item rate; the rest of that
  rarity splits whatever is left evenly.
- the "fixed" (guaranteed-slot) pool drops the lowest rarity entirely and hands its share
  to the middle rarity.
- displayed probabilities are CEILED to 7 decimals, not rounded.

Verified to the last decimal against captures of Gachas_GetCharacterGachaLineup (gacha 1161)
and Gachas_GetPosterGachaLineup (gacha 2519), both gacha_type=Pickup. See _RATES.
"""

import math
import random
from datetime import datetime, timezone
from typing import Optional

from helpers.cache import cache
from models.entities import (
    CharacterRarityProbability,
    GachaLineupItemProbability,
    GachaRollLimit,
    PosterRarityProbability,
)
from models.enums import (
    CharacterRarities,
    GachaCardTypes,
    GachaEmissionFlags,
    GachaTypes,
    PossessionRarities,
    TalentBloomItemTypes,
    ThingTypes,
)

_PRECISION = 7

# rarity -> GachaEmissionFlags bit, per card type. Characters run Rare2/3/4, posters R/SR/SSR.
_CHARACTER_BITS = {
    int(CharacterRarities.Rare2): int(GachaEmissionFlags.Rare2),
    int(CharacterRarities.Rare3): int(GachaEmissionFlags.Rare3),
    int(CharacterRarities.Rare4): int(GachaEmissionFlags.Rare4),
}
_POSTER_BITS = {
    int(PossessionRarities.R): int(GachaEmissionFlags.Rare2),
    int(PossessionRarities.SR): int(GachaEmissionFlags.Rare3),
    int(PossessionRarities.SSR): int(GachaEmissionFlags.Rare4),
}

# (gacha_type, card_type) -> per-rarity totals for the normal and fixed pools, plus the flat
# per-item rate a pickup gets out of its rarity's total.
#
# ONLY gacha_type=Pickup is verified (captures of gachas 1161 and 2519).
#
# Other gacha types demonstrably differ and are NOT covered. Of the 55 banners live in the
# GetAvailableGachas capture only 3 are Pickup (1161, 1641, 2519) -- the rest are types
# 2/7/8/9, and their captured emission flags cannot be reproduced by these numbers
# (e.g. 1916 emits Rare4 only; 1909 keeps Rare2 in its fixed pool). Those banners currently
# fall back to the Pickup rates of their card type, which makes their lineup and emission
# flags WRONG -- 5/55 banners match the capture today. Add a (gacha_type, card_type) entry
# here as captures for each type arrive; lineup + flags both read this table, so they cannot
# drift apart.
_RATES = {
    (int(GachaTypes.Pickup), int(GachaCardTypes.Character)): {
        "normal": {2: 0.82, 3: 0.15, 4: 0.03},
        "fixed": {2: 0.0, 3: 0.97, 4: 0.03},
        "pickup": 0.0075,
    },
    (int(GachaTypes.Pickup), int(GachaCardTypes.Poster)): {
        "normal": {1: 0.80, 2: 0.16, 3: 0.04},
        "fixed": {1: 0.0, 2: 0.96, 3: 0.04},
        "pickup": 0.01,
    },
}

_BY_ID: dict = {}
_CHARACTERS: dict = {}
_POSTERS: dict = {}
_PIECES: dict = {}
_DAI_PIECES: dict = {}


def _build() -> None:
    if not _BY_ID:
        _BY_ID.update({g.id_: g for g in cache.gacha_master})
        _CHARACTERS.update({c.id_: c for c in cache.character_master})
        _POSTERS.update({p.id_: p for p in cache.poster_master})


def _ceil(value: float) -> float:
    """Displayed probabilities are ceiled at 7dp, not rounded -- e.g. 0.82/21 is
    0.0390476190... and the client is told 0.0390477."""
    return math.ceil(value * 10**_PRECISION) / 10**_PRECISION


def _rates(gacha) -> Optional[dict]:
    card = int(gacha.card_type)
    return _RATES.get((int(gacha.gacha_type), card)) or _RATES.get(
        (int(GachaTypes.Pickup), card)
    )


def _rarity_of(gacha, thing) -> Optional[int]:
    lookup = (
        _CHARACTERS
        if int(gacha.card_type) == int(GachaCardTypes.Character)
        else _POSTERS
    )
    row = lookup.get(thing.thing_id)
    return None if row is None else int(row.rarity)


def _pool(gacha, totals: dict, pickup_rate: float) -> list[GachaLineupItemProbability]:
    """One pool's per-item probabilities: pickups take the flat rate, everything else of
    that rarity splits the remainder evenly. Rarities at 0 contribute no items at all.
    """
    by_rarity: dict[int, list] = {}
    for thing in gacha.things:
        rarity = _rarity_of(gacha, thing)
        if rarity is not None and totals.get(rarity, 0.0) > 0.0:
            by_rarity.setdefault(rarity, []).append(thing)

    items: list[GachaLineupItemProbability] = []
    for rarity, things in by_rarity.items():
        pickups = [t for t in things if t.pickup_order is not None]
        rest = [t for t in things if t.pickup_order is None]
        remainder = totals[rarity] - pickup_rate * len(pickups)
        share = remainder / len(rest) if rest else 0.0
        for thing in pickups:
            items.append(
                GachaLineupItemProbability(id=thing.id_, probability=_ceil(pickup_rate))
            )
        for thing in rest:
            items.append(
                GachaLineupItemProbability(id=thing.id_, probability=_ceil(share))
            )
    items.sort(key=lambda i: i.id_)
    return items


def lineup(gacha_master_id: int):
    """``(normal_probabilities, fixed_probabilities, normal_items, fixed_items)`` for a
    banner, or None if the gacha is unknown. Rarity probabilities are returned as the
    card-type-appropriate model (Character* vs Poster*)."""
    _build()
    gacha = _BY_ID.get(gacha_master_id)
    rates = _rates(gacha) if gacha is not None else None
    if gacha is None or rates is None:
        return None

    is_character = int(gacha.card_type) == int(GachaCardTypes.Character)
    model = CharacterRarityProbability if is_character else PosterRarityProbability
    to_probs = lambda totals: [  # noqa: E731 - trivial local shape adapter
        model(rarity=rarity, probability=p) for rarity, p in sorted(totals.items())
    ]
    return (
        to_probs(rates["normal"]),
        to_probs(rates["fixed"]),
        _pool(gacha, rates["normal"], rates["pickup"]),
        _pool(gacha, rates["fixed"], rates["pickup"]),
    )


def emission_flags(gacha_master_id: int) -> tuple[int, int]:
    """``(normal, fixed)`` GachaEmissionFlags bitmasks -- the rarities each pool can emit.
    Derived from the same rate table the lineup uses, so the two can never disagree."""
    _build()
    gacha = _BY_ID.get(gacha_master_id)
    rates = _rates(gacha) if gacha is not None else None
    if gacha is None or rates is None:
        return 0, 0
    bits = (
        _CHARACTER_BITS
        if int(gacha.card_type) == int(GachaCardTypes.Character)
        else _POSTER_BITS
    )
    mask = lambda totals: sum(  # noqa: E731 - trivial local shape adapter
        bit for rarity, bit in bits.items() if totals.get(rarity, 0.0) > 0.0
    )
    return mask(rates["normal"]), mask(rates["fixed"])


def detail_of(gacha_detail_master_id: int):
    """``(gacha, detail)`` for a detail id, or ``(None, None)``. Note RollGacha is addressed
    by DETAIL id -- and its result's ``m_gacha_master_id`` echoes that detail id back, not
    the gacha's (captures: detail 251905 and 116104 both come back verbatim)."""
    _build()
    for gacha in _BY_ID.values():
        for detail in gacha.gacha_details:
            if detail.id_ == gacha_detail_master_id:
                return gacha, detail
    return None, None


def roll_prizes(gacha, detail, rng: Optional[random.Random] = None) -> list:
    """Draw ``prize_count`` things. The last ``fixed_prize_count`` of them come from the
    fixed pool (which excludes the lowest rarity), the rest from the normal pool. Returns
    GachaMaster thing rows."""
    picked = lineup(gacha.id_)
    if picked is None:
        return []
    _, _, normal_items, fixed_items = picked
    things = {t.id_: t for t in gacha.things}
    chooser = rng or random

    def draw(items):
        ids = [i.id_ for i in items]
        weights = [i.probability for i in items]
        return things[chooser.choices(ids, weights=weights, k=1)[0]]

    total = max(0, int(detail.prize_count or 0))
    fixed = min(total, max(0, int(detail.fixed_prize_count or 0)))
    return [draw(normal_items) for _ in range(total - fixed)] + [
        draw(fixed_items) for _ in range(fixed)
    ]


# What a prize pays out when it can no longer be used as a possession.
#
# Posters break through instead of stacking: the first pull creates it at phase 0 and the
# next four each advance a phase, so the 5th acquisition maxes it at phase 4. Only the 6th
# and later convert. Characters have no such step -- any dupe converts immediately.
_DUGONG = 140000  # ジュゴン像, the generic character talent-bloom item
_CHARACTER_DUPE = {
    int(CharacterRarities.Rare2): 1,
    int(CharacterRarities.Rare3): 10,
    int(CharacterRarities.Rare4): 100,
}
_DAI_PIECE = 40  # a Rare4 dupe also pays its own ActorDaiPiece on top of the dugong
_POSTER_DUPE = {
    int(PossessionRarities.R): (130063, 5),  # 金の額縁
    int(PossessionRarities.SR): (130064, 5),  # 明星の額縁
    int(PossessionRarities.SSR): (130064, 50),
}


def dupe_conversion(gacha, thing) -> list[tuple[int, int, int]]:
    """``(thing_type, thing_id, quantity)`` a duplicate pays out instead of the possession.
    Empty when the prize is not a convertible type."""
    _build()
    item = int(ThingTypes.Item)
    if int(gacha.card_type) == int(GachaCardTypes.Character):
        character = _CHARACTERS.get(thing.thing_id)
        if character is None:
            return []
        amount = _CHARACTER_DUPE.get(int(character.rarity))
        if amount is None:
            return []
        out = [(item, _DUGONG, amount)]
        if int(character.rarity) == int(CharacterRarities.Rare4):
            dai = dai_piece_item(thing.thing_id)
            if dai is not None:
                out.append((item, dai, _DAI_PIECE))
        return out

    poster = _POSTERS.get(thing.thing_id)
    if poster is None:
        return []
    frame = _POSTER_DUPE.get(int(poster.rarity))
    return [(item, frame[0], frame[1])] if frame else []


def dai_piece_item(character_master_id: int) -> Optional[int]:
    """The TalentBloom ActorDaiPiece item a Rare4 character's duplicate pays out."""
    if not _DAI_PIECES:
        for row in cache.character_piece_master:
            if int(row.talent_bloom_item_type) == int(
                TalentBloomItemTypes.ActorDaiPiece
            ):
                _DAI_PIECES[row.character_master_id] = row.item_master_id
    return _DAI_PIECES.get(character_master_id)


def poster_max_phase(poster_master_id: int) -> int:
    """How far a poster can be broken through -- each dupe of an owned, un-maxed poster
    advances it one phase instead of granting a second copy."""
    _build()
    poster = _POSTERS.get(poster_master_id)
    return int(getattr(poster, "poster_breakthrough_max_phase", 0) or 0)


def piece_item(character_master_id: int) -> Optional[int]:
    """The TalentBloom ActorPiece item a character converts to, per CharacterPieceMaster."""
    if not _PIECES:
        for row in cache.character_piece_master:
            if int(row.talent_bloom_item_type) == int(TalentBloomItemTypes.ActorPiece):
                _PIECES[row.character_master_id] = row.item_master_id
    return _PIECES.get(character_master_id)


# a Rare4 character prize rides along with a pile of its own ActorPiece. Captures show the
# banner's pickup paying 4x what an off-banner Rare4 does:
#   142490 (the pickup) -> 400, both as a new pull and as a dupe
#   140410, 142030      -> 100
# CharacterPieceMaster is byte-identical for all three, so the split is banner-relative,
# not character-intrinsic -- pickup_order is the only thing that separates them.
_PIECE_PICKUP = 400
_PIECE_REGULAR = 100


def piece_bonus(gacha, thing) -> list[tuple[int, int, int]]:
    """``(thing_type, thing_id, quantity)`` for the piece bonus attached to a prize, as
    ``additional_received_things``. Empty for anything but a Rare4 character.

    TODO: only Rare4 is observed. Every Rare2/Rare3 character in the captures arrived as a
    dupe, so whether a *new* low-rarity character also pays pieces is unknown -- returning
    nothing for them is a guess, just a conservative one.
    """
    _build()
    if int(gacha.card_type) != int(GachaCardTypes.Character):
        return []
    character = _CHARACTERS.get(thing.thing_id)
    if character is None or int(character.rarity) != int(CharacterRarities.Rare4):
        return []
    item = piece_item(thing.thing_id)
    if item is None:
        return []
    amount = _PIECE_PICKUP if thing.pickup_order is not None else _PIECE_REGULAR
    return [(int(ThingTypes.Item), item, amount)]


def active_gacha_ids(now: Optional[datetime] = None) -> list[int]:
    """Banner ids currently inside their start/end window, in master ``order``."""
    _build()
    at = now or datetime.now(timezone.utc)
    live = []
    for gacha in _BY_ID.values():
        try:
            start = datetime.fromisoformat(gacha.start_date)
            end = datetime.fromisoformat(gacha.end_date)
        except (TypeError, ValueError):
            continue
        if start <= at <= end:
            live.append(gacha)
    live.sort(key=lambda g: (g.order, g.id_))
    return [g.id_ for g in live]


def roll_limits(gacha_master_id: int, used: dict[int, int]) -> list[GachaRollLimit]:
    """Remaining rolls for each of a banner's *limited* details. Details with neither a
    daily nor an overall limit are omitted entirely -- captures show banners whose every
    detail is unlimited reporting an empty list. ``used`` maps detail id -> rolls spent.
    """
    _build()
    gacha = _BY_ID.get(gacha_master_id)
    if gacha is None:
        return []
    out: list[GachaRollLimit] = []
    for detail in gacha.gacha_details:
        limits = [
            n
            for n in (detail.daily_roll_limit, detail.overall_roll_limit)
            if n is not None
        ]
        if not limits:
            continue
        left = min(limits) - used.get(detail.id_, 0)
        out.append(
            GachaRollLimit(gacha_detail_master_id=detail.id_, roll_left=max(0, left))
        )
    return out
