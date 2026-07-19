from typing import Optional

from db.query import ExecutableQuery, SelectQuery
from models.database import CharacterBaseModel, InboxModel


def get_character_base(
    user_id: int, base_master_id: int
) -> SelectQuery[CharacterBaseModel]:
    return SelectQuery(
        CharacterBaseModel,
        'SELECT * FROM "character_base" WHERE "userId" = $1 AND "characterBaseMasterId" = $2 LIMIT 1',
        user_id,
        base_master_id,
    )


def create_character_base(
    user_id: int,
    row_id: int,
    base_master_id: int,
    costume_master_id: Optional[int],
    portal_character_id: int,
) -> ExecutableQuery:
    return ExecutableQuery(
        'INSERT INTO "character_base" '
        '("userId", "id", "characterBaseMasterId", "costumeMasterId", "portalCharacterId") '
        "VALUES ($1, $2, $3, $4, $5)",
        user_id,
        row_id,
        base_master_id,
        costume_master_id,
        portal_character_id,
    )


def create_character(
    user_id: int, row_id: int, master_id: int, character_base_id: int
) -> ExecutableQuery:
    return ExecutableQuery(
        'INSERT INTO "character" '
        '("userId", "id", "characterMasterId", "characterBaseId", "level", "senseLevel", "selectionType") '
        "VALUES ($1, $2, $3, $4, 1, 1, 1)",
        user_id,
        row_id,
        master_id,
        character_base_id,
    )


def create_accessory(
    user_id: int, row_id: int, master_id: int, effects: list
) -> ExecutableQuery:
    return ExecutableQuery(
        'INSERT INTO "accessory" '
        '("userId", "id", "accessoryMasterId", "level", "accessoryEffects") '
        "VALUES ($1, $2, $3, 1, $4)",
        user_id,
        row_id,
        master_id,
        effects,
    )


def add_stamina(user_id: int, amount: int) -> ExecutableQuery:
    return ExecutableQuery(
        'UPDATE "user" SET "currentStamina" = "currentStamina" + $2 WHERE "userId" = $1',
        user_id,
        amount,
    )


def grant_possession(
    table: str, master_col: str, user_id: int, row_id: int, master_id: int, extra: dict
) -> ExecutableQuery:
    # table / master_col / extra keys come from a hardcoded ThingType map, never user input
    cols = ['"userId"', '"id"', f'"{master_col}"'] + [f'"{k}"' for k in extra]
    vals = [user_id, row_id, master_id, *extra.values()]
    placeholders = ", ".join(f"${i + 1}" for i in range(len(vals)))
    return ExecutableQuery(
        f'INSERT INTO "{table}" ({", ".join(cols)}) VALUES ({placeholders})', *vals
    )


def grant_collection(
    table: str, array_col: str, user_id: int, master_id: int
) -> ExecutableQuery:
    # append master_id to the per-user singleton's json array (creating the row if absent);
    # jsonb is built in SQL so no python-list -> json codec is needed
    return ExecutableQuery(
        f"WITH upd AS ("
        f'  UPDATE "{table}" SET "{array_col}" = '
        f"    (COALESCE(\"{array_col}\"::jsonb, '[]'::jsonb) || jsonb_build_array($2::bigint)) "
        f'  WHERE "userId" = $1 AND NOT '
        f"    (COALESCE(\"{array_col}\"::jsonb, '[]'::jsonb) @> jsonb_build_array($2::bigint)) "
        f"  RETURNING 1"
        f") "
        f'INSERT INTO "{table}" ("userId", "id", "{array_col}") '
        f"SELECT $1, $1, jsonb_build_array($2::bigint) "
        f'WHERE NOT EXISTS (SELECT 1 FROM "{table}" WHERE "userId" = $1)',
        user_id,
        master_id,
    )


def get_inboxes_by_ids(user_id: int, ids) -> SelectQuery[InboxModel]:
    return SelectQuery(
        InboxModel,
        'SELECT * FROM "inbox" WHERE "userId" = $1 AND "id" = ANY($2::bigint[])',
        user_id,
        list(ids),
    )


def receive_inbox(user_id: int, inbox_id: int, now: int) -> ExecutableQuery:
    return ExecutableQuery(
        'UPDATE "inbox" SET "hasReceived" = true, "receivedAt" = $3 '
        'WHERE "userId" = $1 AND "id" = $2 AND "hasReceived" = false',
        user_id,
        inbox_id,
        now,
    )
