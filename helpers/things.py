"""Granting "things" (rewards) -- the item/currency analog of sekai's materials. A grant
adds any ThingType to its proper per-user table (currency, item stock, stamina, a json
collection, or an owned possession row) and returns a ReceivedThing describing it.
"""

import random
from typing import Optional

from db.user import (
    add_currency,
    add_stamina,
    create_accessory,
    create_character,
    create_character_base,
    get_character_base,
    grant_collection,
    grant_possession,
    increment_item_stock,
)
from helpers.cache import cache
from models import ReceivedThing
from models.enums import ThingTypes as T

# possession tables -- one owned row per unit: ThingType -> (table, masterId col, fixed extra cols).
# Character/Accessory are handled separately (they need masterdata-derived fields).
_POSSESSION = {
    T.Poster: ("poster", "posterMasterId", {}),
    T.Costume: ("costume", "costumeMasterId", {}),
    T.Trophy: ("trophy", "trophyMasterId", {}),
    T.Nameplate: ("nameplate", "namePlateMasterId", {}),
    T.Music: ("music", "musicMasterId", {"isPossession": True}),
    T.Decoration: ("decoration", "decorationMasterId", {}),
    T.AlbumTheme: ("album_theme", "albumThemeMasterId", {}),
}
# per-user singleton collections -- masterId appended to a json array: ThingType -> (table, array col)
_COLLECTION = {
    T.Stamp: ("stamp", "stampMasterIds"),
    T.NameColor: ("name_color", "nameColorMasterIds"),
    T.Bomb: ("bomb", "bombMasterIds"),
    T.Note: ("note", "noteMasterIds"),
    T.NameBaseColor: ("name_base_color", "nameBaseColorMasterIds"),
    T.IconFrame: ("icon_frame", "iconFrameMasterIds"),
    T.HomeSkin: ("home_skin", "homeSkinMasterIds"),
}
# ThingType -> the per-user entity type its grant writes (so callers can build `present`)
_PRESENT_TYPE = {
    T.Coin: "Currency",
    T.Jewel: "Currency",
    T.Item: "Item",
    T.Stamina: "User",
    T.Character: "Character",
    T.Poster: "Poster",
    T.Accessory: "Accessory",
    T.Costume: "Costume",
    T.Trophy: "Trophy",
    T.Nameplate: "Nameplate",
    T.Music: "Music",
    T.Decoration: "Decoration",
    T.AlbumTheme: "AlbumTheme",
    T.Stamp: "Stamp",
    T.NameColor: "NameColor",
    T.Bomb: "Bomb",
    T.Note: "Note",
    T.NameBaseColor: "NameBaseColor",
    T.IconFrame: "IconFrame",
    T.HomeSkin: "HomeSkin",
}


def _random_id() -> int:
    return random.randint(1_000_000, 9_999_999_999)


_masters: dict = {}


def _by_id(table: str) -> dict:
    if table not in _masters:
        _masters[table] = {r.id_: r for r in getattr(cache, table)}
    return _masters[table]


async def _grant_character(conn, user_id: int, character_master_id: int) -> None:
    # Character.characterBaseId points at an owned CharacterBase (shared across a
    # character's variants); resolve it via CharacterMaster.character_base_master_id.
    master = _by_id("character_master").get(character_master_id)
    base_master_id = master.character_base_master_id if master is not None else None
    base_id = 0
    if base_master_id is not None:
        existing = await conn.fetchrow(get_character_base(user_id, base_master_id))
        if existing is not None:
            base_id = existing.id
        else:
            base_id = _random_id()
            bm = _by_id("character_base_master").get(base_master_id)
            costume = bm.default_costume_master_id if bm is not None else None
            await conn.execute(
                create_character_base(
                    user_id, base_id, base_master_id, costume, character_master_id
                )
            )
    await conn.execute(
        create_character(user_id, _random_id(), character_master_id, base_id)
    )


async def _grant_accessory(conn, user_id: int, accessory_master_id: int) -> None:
    # fixed effects stay derived from AccessoryMaster on demand; only the rolled random
    # effects (one per random_effect_group) are persisted in accessory_effects.
    master = _by_id("accessory_master").get(accessory_master_id)
    groups = _by_id("random_effect_group_master")
    effects: list = []
    if master is not None:
        for group_id in master.random_effect_groups or []:
            group = groups.get(group_id)
            if group is not None and group.accessory_effects:
                effects.append(random.choice(group.accessory_effects))
    await conn.execute(
        create_accessory(user_id, _random_id(), accessory_master_id, effects)
    )


def present_type(thing_type: int) -> Optional[str]:
    """The per-user entity type a grant of ``thing_type`` writes (for `present`), or None."""
    try:
        return _PRESENT_TYPE.get(T(int(thing_type)))
    except ValueError:
        return None


async def grant_thing(
    conn, user_id: int, thing_type: int, thing_id: int, quantity: int
) -> ReceivedThing:
    """Add one thing to its proper per-user table. Returns the ReceivedThing describing it."""
    t = T(int(thing_type))
    if t == T.Coin:
        await conn.execute(add_currency(user_id, coin=quantity))
    elif t == T.Jewel:
        await conn.execute(add_currency(user_id, free_jewel=quantity))
    elif t == T.Item:
        await conn.execute(increment_item_stock(user_id, thing_id, quantity))
    elif t == T.Stamina:
        await conn.execute(add_stamina(user_id, quantity))
    elif t == T.Character:
        for _ in range(max(1, int(quantity))):
            await _grant_character(conn, user_id, thing_id)
    elif t == T.Accessory:
        for _ in range(max(1, int(quantity))):
            await _grant_accessory(conn, user_id, thing_id)
    elif t in _COLLECTION:
        table, array_col = _COLLECTION[t]
        await conn.execute(grant_collection(table, array_col, user_id, thing_id))
    elif t in _POSSESSION:
        table, master_col, extra = _POSSESSION[t]
        for _ in range(max(1, int(quantity))):  # one owned row per unit
            await conn.execute(
                grant_possession(
                    table, master_col, user_id, _random_id(), thing_id, extra
                )
            )
    return ReceivedThing(type=int(t), id_=thing_id, quantity=quantity, sent_inbox=False)


async def grant_things(conn, user_id: int, things) -> list:
    """Grant many ``(thing_type, thing_id, quantity)`` tuples. Returns the ReceivedThing[]."""
    return [await grant_thing(conn, user_id, tt, tid, q) for tt, tid, q in things]
