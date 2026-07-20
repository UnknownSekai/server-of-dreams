from db.query import ExecutableQuery, SelectQuery
from models.database import ActiveLiveModel, SequenceValueModel


def next_live_id() -> SelectQuery[SequenceValueModel]:
    # collision-free owned-live id, allocated from a Postgres sequence (see live_id_seq)
    return SelectQuery(SequenceValueModel, "SELECT nextval('live_id_seq') AS value")


def update_player_rate(user_id: int, rate: float) -> ExecutableQuery:
    return ExecutableQuery(
        'UPDATE "user_profile" SET "playerRate" = $2 WHERE "userId" = $1',
        user_id,
        rate,
    )


def update_music_releases(
    user_id: int, changes: list[tuple[int, bool, int]]
) -> ExecutableQuery:
    """Batch stella/olivier release updates for many music rows into one statement
    (changes = [(music_id, stella_released, olivier_status), ...]; must be non-empty).
    """
    rows: list[str] = []
    args: list = [user_id]
    for music_id, stella_released, olivier_status in changes:
        n = len(args)
        rows.append(f"(${n + 1}::bigint, ${n + 2}::boolean, ${n + 3}::integer)")
        args.extend((music_id, stella_released, olivier_status))
    return ExecutableQuery(
        'UPDATE "music" AS m SET "stellaReleased" = v.stella, '
        '"olivierReleaseStatus" = v.status '
        f'FROM (VALUES {", ".join(rows)}) AS v(id, stella, status) '
        'WHERE m."userId" = $1 AND m."id" = v.id',
        *args,
    )


def delete_active_lives(user_id: int) -> ExecutableQuery:
    return ExecutableQuery('DELETE FROM "active_live" WHERE "userId" = $1', user_id)


def create_active_live(
    user_id: int,
    live_id: int,
    live_master_id: int,
    party_id: int,
    live_setting_master_id: int = 0,
    stamina_spent: bool = False,
) -> ExecutableQuery:
    return ExecutableQuery(
        'INSERT INTO "active_live" '
        '("userId", "id", "liveMasterId", "partyId", "liveSettingMasterId", "staminaSpent") '
        "VALUES ($1, $2, $3, $4, $5, $6)",
        user_id,
        live_id,
        live_master_id,
        party_id,
        live_setting_master_id,
        stamina_spent,
    )


def get_active_live(user_id: int) -> SelectQuery[ActiveLiveModel]:
    return SelectQuery(
        ActiveLiveModel, 'SELECT * FROM "active_live" WHERE "userId" = $1', user_id
    )


def update_live_result(
    user_id: int,
    live_master_id: int,
    times_completed: int,
    achievement_rate: float,
    notation_rate: float,
    clear_lamp: int,
    rate_grade: int,
) -> ExecutableQuery:
    # best-of merge is decided by the caller; this just writes the row for (userId, liveMasterId)
    return ExecutableQuery(
        'UPDATE "live" SET "timesCompleted" = $3, "achievementRate" = $4, '
        '"notationRate" = $5, "clearLamp" = $6, "rateGrade" = $7 '
        'WHERE "userId" = $1 AND "liveMasterId" = $2',
        user_id,
        live_master_id,
        times_completed,
        achievement_rate,
        notation_rate,
        clear_lamp,
        rate_grade,
    )
