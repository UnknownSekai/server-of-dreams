from typing import Optional

from db.query import ExecutableQuery, SelectQuery
from models.database import (
    ExchangeLimitModel,
    MarketModel,
    MarketThingModel,
    MusicModel,
    PartySlotModel,
    PermanentMarketThingModel,
    UserModel,
)


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


def update_birth_date(user_id: int, birth_date: Optional[int]) -> ExecutableQuery:
    """Set the caller's birth date (epoch microseconds, or NULL to clear it)."""
    return ExecutableQuery(
        'UPDATE "user_preference" SET "birthDate" = $2 WHERE "userId" = $1',
        user_id,
        birth_date,
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


def replace_market_things(
    user_id: int, frames: list[tuple[int, int, Optional[int]]]
) -> ExecutableQuery:
    """Swap in a freshly rolled market lineup, as ``(frame_number, master_id, discount)``.

    The old frames are dropped in the same statement rather than updated in place: a refresh
    is a whole new market, and carrying a stale ``hasPurchased`` across it would let one
    purchase block whichever frame it landed on forever.
    """
    if not frames:
        return ExecutableQuery(
            'DELETE FROM "market_thing" WHERE "userId" = $1', user_id
        )
    rows: list[str] = []
    args: list = [user_id]
    for frame_number, master_id, discount in frames:
        args.extend((frame_number, master_id, discount))
        n = len(args)
        rows.append(f"($1::bigint, ${n - 2}::bigint, ${n - 1}::bigint, ${n}::bigint)")
    return ExecutableQuery(
        'WITH d AS (DELETE FROM "market_thing" WHERE "userId" = $1) '
        'INSERT INTO "market_thing" '
        '("userId", "frameNumber", "marketFrameThingMasterId", "discountPercent") '
        f"VALUES {', '.join(rows)}",
        *args,
    )


def purchase_market_thing(
    user_id: int, frame_number: int
) -> SelectQuery[MarketThingModel]:
    """Claim one market frame, returning it -- or nothing if it was already bought.

    Guarded on ``hasPurchased`` being false inside the UPDATE, so two concurrent buys of the
    same frame can't both win: the loser gets 0 rows and the caller charges nothing.
    """
    return SelectQuery(
        MarketThingModel,
        'UPDATE "market_thing" SET "hasPurchased" = TRUE '
        'WHERE "userId" = $1 AND "frameNumber" = $2 AND "hasPurchased" = FALSE '
        "RETURNING *",
        user_id,
        frame_number,
    )


def roll_over_market(
    user_id: int, now: int, new_id: int, reset_at: int
) -> SelectQuery[MarketModel]:
    """Move the market into the current period: zero ``refreshTimes``, stamp
    ``lastRefreshedAt``.

    Returns a row only when the period actually turned over -- the market was last stamped
    before ``reset_at`` (the most recent 11:00/23:00 JST boundary), or the user has no market
    yet. An empty result means the stored lineup is still current and the caller leaves it
    alone; rolling the new frames is the caller's job.
    """
    return SelectQuery(
        MarketModel,
        "WITH upd AS ("
        '  UPDATE "market" SET "lastRefreshedAt" = $2, "refreshTimes" = 0 '
        '  WHERE "userId" = $1 AND "lastRefreshedAt" < $4 '
        "  RETURNING *"
        "), ins AS ("
        '  INSERT INTO "market" ("userId", "id", "lastRefreshedAt", "refreshTimes") '
        "  SELECT $1, $3, $2, 0 "
        "  WHERE NOT EXISTS (SELECT 1 FROM upd) "
        '    AND NOT EXISTS (SELECT 1 FROM "market" WHERE "userId" = $1) '
        "  RETURNING *"
        ") "
        "SELECT * FROM upd UNION ALL SELECT * FROM ins",
        user_id,
        now,
        new_id,
        reset_at,
    )


def consume_market_refresh(
    user_id: int, now: int, new_id: int, reset_at: int, max_refreshes: int
) -> SelectQuery[MarketModel]:
    """Count one paid market refresh against the per-period ceiling, returning the market row
    with its new ``refreshTimes`` -- or nothing when the ceiling is already reached.

    A market last stamped before ``reset_at`` belongs to the previous period, so its tally
    restarts at 1 rather than continuing. Folding that into the same statement as the
    increment and the cap check is what stops a user being charged the 50-jewel rate on a
    fresh market, or racing two requests into an eleventh refresh.
    """
    counted = 'CASE WHEN "lastRefreshedAt" < $4 THEN 1 ELSE "refreshTimes" + 1 END'
    return SelectQuery(
        MarketModel,
        "WITH upd AS ("
        f'  UPDATE "market" SET "refreshTimes" = {counted}, "lastRefreshedAt" = $2 '
        '  WHERE "userId" = $1 '
        f"    AND ({counted}) <= $5 "
        "  RETURNING *"
        "), ins AS ("
        '  INSERT INTO "market" ("userId", "id", "lastRefreshedAt", "refreshTimes") '
        "  SELECT $1, $3, $2, 1 "
        "  WHERE NOT EXISTS (SELECT 1 FROM upd) "
        '    AND NOT EXISTS (SELECT 1 FROM "market" WHERE "userId" = $1) '
        "    AND 1 <= $5 "
        "  RETURNING *"
        ") "
        "SELECT * FROM upd UNION ALL SELECT * FROM ins",
        user_id,
        now,
        new_id,
        reset_at,
        max_refreshes,
    )


def consume_exchange_limit(
    user_id: int,
    exchange_shop_thing_id: int,
    quantity: int,
    limit: int,
    replace_type: int,
    until: Optional[int],
    now: int,
    new_id: int,
) -> SelectQuery[ExchangeLimitModel]:
    """Count ``quantity`` more exchanges of one shop entry against its cap, creating the
    tracking row on first purchase. Returns the updated row, or nothing when the cap would
    be exceeded -- so the caller can reject the exchange before charging for it.

    The cap is enforced in the UPDATE's WHERE clause rather than read-then-written, because
    it is the only thing stopping a limited entry from being bought repeatedly. A row whose
    ``until`` has already passed is a spent period: it resets to ``quantity`` instead of
    blocking, which is how Daily/Weekly/Monthly entries come back.
    """
    expired = 'CASE WHEN "until" IS NOT NULL AND "until" <= $7 THEN $3 ELSE "exchangedCount" + $3 END'
    return SelectQuery(
        ExchangeLimitModel,
        "WITH upd AS ("
        f'  UPDATE "exchange_limit" SET "exchangedCount" = {expired}, '
        '    "until" = $6, "replaceType" = $5 '
        '  WHERE "userId" = $1 AND "exchangeShopThingId" = $2 '
        f"    AND ({expired}) <= $4 "
        "  RETURNING *"
        "), ins AS ("
        '  INSERT INTO "exchange_limit" ("userId", "id", "exchangeShopThingId", '
        '    "replaceType", "exchangedCount", "until") '
        "  SELECT $1, $8, $2, $5, $3, $6 "
        "  WHERE NOT EXISTS (SELECT 1 FROM upd) "
        '    AND NOT EXISTS (SELECT 1 FROM "exchange_limit" '
        '      WHERE "userId" = $1 AND "exchangeShopThingId" = $2) '
        "    AND $3 <= $4 "
        "  RETURNING *"
        ") "
        "SELECT * FROM upd UNION ALL SELECT * FROM ins",
        user_id,
        exchange_shop_thing_id,
        quantity,
        limit,
        replace_type,
        until,
        now,
        new_id,
    )


def consume_permanent_market_limit(
    user_id: int, master_id: int, quantity: int, limit: int
) -> SelectQuery[PermanentMarketThingModel]:
    """The permanent market's equivalent of :func:`consume_exchange_limit`. These entries
    never reset, so there is no period to expire and the cap is simply lifetime. Returns
    nothing when the purchase would exceed it."""
    return SelectQuery(
        PermanentMarketThingModel,
        "WITH upd AS ("
        '  UPDATE "permanent_market_thing" SET "purchaseCount" = "purchaseCount" + $3 '
        '  WHERE "userId" = $1 AND "permanentMarketThingMasterId" = $2 '
        '    AND "purchaseCount" + $3 <= $4 '
        "  RETURNING *"
        "), ins AS ("
        '  INSERT INTO "permanent_market_thing" '
        '    ("userId", "permanentMarketThingMasterId", "purchaseCount") '
        "  SELECT $1, $2, $3 "
        "  WHERE NOT EXISTS (SELECT 1 FROM upd) "
        '    AND NOT EXISTS (SELECT 1 FROM "permanent_market_thing" '
        '      WHERE "userId" = $1 AND "permanentMarketThingMasterId" = $2) '
        "    AND $3 <= $4 "
        "  RETURNING *"
        ") "
        "SELECT * FROM upd UNION ALL SELECT * FROM ins",
        user_id,
        master_id,
        quantity,
        limit,
    )


def release_music_olivier(
    user_id: int, music_master_id: int, purchasable: int, released: int
) -> SelectQuery[MusicModel]:
    """Buy a song's Olivier chart, returning the music row -- or nothing if it wasn't for
    sale.

    Guarded on the stored status being exactly ``purchasable``: Olivier is only purchasable
    once its level is within what the user has already cleared (see helpers/music_unlock),
    and re-buying an already-Released chart must not charge a second ticket. Both cases fall
    out of the same WHERE.
    """
    return SelectQuery(
        MusicModel,
        'UPDATE "music" SET "olivierReleaseStatus" = $4 '
        'WHERE "userId" = $1 AND "musicMasterId" = $2 AND "olivierReleaseStatus" = $3 '
        "RETURNING *",
        user_id,
        music_master_id,
        purchasable,
        released,
    )


def record_jewel_shop_purchase(
    user_id: int,
    jewel_shop_item_master_id: int,
    new_id: int,
    re_purchase_date: Optional[int],
) -> ExecutableQuery:
    """Count one jewel-pack purchase, creating the row on first buy. ``purchaseCount`` is
    the per-period tally the pack's replace type resets; ``totalPurchaseCount`` is lifetime.
    """
    return ExecutableQuery(
        "WITH upd AS ("
        '  UPDATE "jewel_shop" SET "purchaseCount" = "purchaseCount" + 1, '
        '    "totalPurchaseCount" = "totalPurchaseCount" + 1, "rePurchaseDate" = $4 '
        '  WHERE "userId" = $1 AND "jewelShopItemMasterId" = $2 RETURNING 1'
        ") "
        'INSERT INTO "jewel_shop" ("userId", "id", "jewelShopItemMasterId", '
        '  "purchaseCount", "totalPurchaseCount", "rePurchaseDate") '
        "SELECT $1, $3, $2, 1, 1, $4 WHERE NOT EXISTS (SELECT 1 FROM upd)",
        user_id,
        jewel_shop_item_master_id,
        new_id,
        re_purchase_date,
    )


def touch_viewed_shop(
    user_id: int,
    category: int,
    exchange_shop_master_id: Optional[int],
    now: int,
    new_id: int,
) -> ExecutableQuery:
    """Mark a shop tab as seen at ``now``, creating the row the first time it is opened.

    A tab is identified by (category, exchangeShopMasterId) and that master id is nullable,
    so the match uses IS NOT DISTINCT FROM -- plain ``=`` never matches NULL and would
    insert a fresh duplicate row on every view of a category-level tab.
    """
    return ExecutableQuery(
        "WITH upd AS ("
        '  UPDATE "viewed_shop" SET "lastViewedAt" = $4 '
        '  WHERE "userId" = $1 AND "viewedShopCategory" = $2 '
        '    AND "exchangeShopMasterId" IS NOT DISTINCT FROM $3 RETURNING 1'
        ") "
        'INSERT INTO "viewed_shop" '
        '  ("userId", "id", "exchangeShopMasterId", "lastViewedAt", "viewedShopCategory") '
        "SELECT $1, $5, $3, $4, $2 WHERE NOT EXISTS (SELECT 1 FROM upd)",
        user_id,
        category,
        exchange_shop_master_id,
        now,
        new_id,
    )
