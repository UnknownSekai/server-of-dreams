from typing import Optional

from db.query import SelectQuery
from models.database import UserModel


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
