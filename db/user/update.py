from typing import Optional

from db.query import ExecutableQuery, SelectQuery
from models.database import PartySlotModel, UserModel


def update_party_slots(user_id: int, slots: list[PartySlotModel]) -> ExecutableQuery:
    """Batch character/poster/accessory/flags updates for many party slots into one
    statement (``slots`` must be non-empty). Rows are matched on (userId, id) -- an edit
    never reassigns a slot's partyId or position, and never creates a slot.
    """
    rows: list[str] = []
    args: list = [user_id]
    for s in slots:
        n = len(args)
        rows.append(
            f"(${n + 1}::bigint, ${n + 2}::bigint, ${n + 3}::bigint, "
            f"${n + 4}::bigint, ${n + 5}::bigint)"
        )
        args.extend(
            (s.id, s.characterId, s.posterId, s.accessoryId, s.bonusAbilityEnableFlags)
        )
    return ExecutableQuery(
        'UPDATE "party_slot" AS s SET "characterId" = v.character_id, '
        '"posterId" = v.poster_id, "accessoryId" = v.accessory_id, '
        '"bonusAbilityEnableFlags" = v.flags '
        f"FROM (VALUES {', '.join(rows)}) AS v(id, character_id, poster_id, accessory_id, flags) "
        'WHERE s."userId" = $1 AND s."id" = v.id',
        *args,
    )


def update_party_slot_positions(
    user_id: int, positions: list[tuple[int, int]]
) -> ExecutableQuery:
    """Batch position reassignment for many party slots into one statement
    (``positions`` = [(slot_id, position), ...]; must be non-empty).
    """
    rows: list[str] = []
    args: list = [user_id]
    for slot_id, position in positions:
        n = len(args)
        rows.append(f"(${n + 1}::bigint, ${n + 2}::bigint)")
        args.extend((slot_id, position))
    return ExecutableQuery(
        'UPDATE "party_slot" AS s SET "position" = v.position '
        f"FROM (VALUES {', '.join(rows)}) AS v(id, position) "
        'WHERE s."userId" = $1 AND s."id" = v.id',
        *args,
    )


def update_party_leader(user_id: int, party_id: int, position: int) -> ExecutableQuery:
    return ExecutableQuery(
        'UPDATE "party" SET "leaderPosition" = $3 WHERE "userId" = $1 AND "id" = $2',
        user_id,
        party_id,
        position,
    )


def update_party_name(user_id: int, party_id: int, name: str) -> ExecutableQuery:
    return ExecutableQuery(
        'UPDATE "party" SET "name" = $3 WHERE "userId" = $1 AND "id" = $2',
        user_id,
        party_id,
        name,
    )


def breakthrough_poster(
    user_id: int, poster_id: int, max_phase: int
) -> ExecutableQuery:
    """Push one owned poster up a breakthrough phase, capped at ``max_phase``. The cap is
    enforced in SQL so a concurrent roll can't push a maxed poster past it."""
    return ExecutableQuery(
        'UPDATE "poster" SET "breakthroughPhase" = "breakthroughPhase" + 1 '
        'WHERE "userId" = $1 AND "id" = $2 AND "breakthroughPhase" < $3',
        user_id,
        poster_id,
        max_phase,
    )


def add_gacha_rolls(
    user_id: int, gacha_master_id: int, delta: int, new_id: int
) -> ExecutableQuery:
    """Add ``delta`` to a banner's lifetime roll count, creating the row on first roll."""
    return ExecutableQuery(
        "WITH upd AS ("
        '  UPDATE "gacha" SET "rollCount" = "rollCount" + $3 '
        '  WHERE "userId" = $1 AND "gachaMasterId" = $2 RETURNING 1'
        ") "
        'INSERT INTO "gacha" ("userId", "id", "gachaMasterId", "rollCount") '
        "SELECT $1, $4, $2, $3 WHERE NOT EXISTS (SELECT 1 FROM upd)",
        user_id,
        gacha_master_id,
        delta,
        new_id,
    )


def add_gacha_historys(
    user_id: int, card_type: int, master_ids: list[int], created_at: int
) -> ExecutableQuery:
    """Append one history row per prize pulled (``master_ids`` must be non-empty). Every
    prize of a roll shares that roll's timestamp, as the captures show."""
    rows: list[str] = []
    args: list = [user_id, card_type, created_at]
    for master_id in master_ids:
        args.append(master_id)
        rows.append(f"($1::bigint, $2::bigint, ${len(args)}::bigint, $3::bigint)")
    return ExecutableQuery(
        'INSERT INTO "gacha_history" ("userId", "cardType", "masterId", "createdAt") '
        f"VALUES {', '.join(rows)}",
        *args,
    )


def set_gacha_selected_things(
    user_id: int, gacha_master_id: int, thing_ids: list[int]
) -> ExecutableQuery:
    """Replace the caller's pickup selection for one gacha. There is no unique constraint on
    (userId, gachaMasterId), so the old row is deleted in the same statement rather than
    leaning on ON CONFLICT -- re-selecting must not accumulate duplicate rows.
    """
    return ExecutableQuery(
        'WITH d AS (DELETE FROM "gacha_selected_thing" '
        'WHERE "userId" = $1 AND "gachaMasterId" = $2) '
        'INSERT INTO "gacha_selected_thing" ("userId", "gachaMasterId", "gachaThingIds") '
        "VALUES ($1, $2, $3)",
        user_id,
        gacha_master_id,
        thing_ids,
    )


def update_multi_party(user_id: int, party_id: int) -> ExecutableQuery:
    return ExecutableQuery(
        'UPDATE "user_preference" SET "multiPartyId" = $2 WHERE "userId" = $1',
        user_id,
        party_id,
    )


def adjust_user_stamina_atomic(
    user_id: int,
    delta: int,
    max_stamina: int,
    interval_micros: int,
    now_micros: int,
    auto_max_clamp: bool = False,
) -> SelectQuery[UserModel]:
    """Atomically recover-then-adjust the caller's stamina in a single statement, so
    concurrent requests can't corrupt it. ``currentStamina`` + ``maxStaminaRestoredAt``
    (the "full at" time) are the stored state; effective stamina is recomputed from that
    timestamp before ``delta`` is applied, then ``maxStaminaRestoredAt`` is rescheduled.

    - ``delta`` may be positive (recover) or negative (consume).
    - Strict mode (``auto_max_clamp=False``): succeeds only if the result is >= 0 and, for a
      positive delta, <= ``max_stamina``. Consuming below 0 fails (no row returned).
    - Clamp mode: a positive delta that would exceed ``max_stamina`` is capped to it.
    - Recovery items may overfill above max; effective stamina at/above max never regenerates.
    - Returns 1 row (the updated User) on success, 0 rows on failure.
    """
    return SelectQuery(
        UserModel,
        """
        WITH p AS (
            SELECT $1::bigint AS uid, $2::int AS delta, $3::int AS maxst,
                   $4::bigint AS interval, $5::bigint AS now, $6::boolean AS clamp
        ),
        eff AS (
            SELECT u.*, p.delta, p.maxst, p.interval, p.now, p.clamp,
                CASE
                    WHEN u."currentStamina" >= p.maxst THEN u."currentStamina"
                    WHEN p.interval <= 0 OR p.now >= u."maxStaminaRestoredAt" THEN p.maxst
                    ELSE GREATEST(
                        0,
                        p.maxst - CEIL((u."maxStaminaRestoredAt" - p.now)::numeric / p.interval)::int
                    )
                END AS effective
            FROM "user" u JOIN p ON u."userId" = p.uid
        ),
        calc AS (
            SELECT e.*,
                CASE WHEN e.delta > 0 AND e.clamp
                     THEN LEAST(e.maxst, e.effective + e.delta)
                     ELSE e.effective + e.delta
                END AS new_st
            FROM eff e
        )
        UPDATE "user" u2 SET
            "currentStamina" = c.new_st,
            "maxStaminaRestoredAt" = CASE
                WHEN c.new_st >= c.maxst THEN c.now
                WHEN c.interval > 0 THEN c.now + (c.maxst - c.new_st)::bigint * c.interval
                ELSE c.now
            END
        FROM calc c
        WHERE u2."userId" = c."userId"
          AND c.new_st >= 0
          AND (c.clamp OR c.delta <= 0 OR c.new_st <= c.maxst)
        RETURNING u2.*
        """,
        user_id,
        delta,
        max_stamina,
        interval_micros,
        now_micros,
        auto_max_clamp,
    )
