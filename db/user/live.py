from db.query import ExecutableQuery, SelectQuery
from models.database import ActiveLiveModel


def delete_active_lives(user_id: int) -> ExecutableQuery:
    return ExecutableQuery('DELETE FROM "active_live" WHERE "userId" = $1', user_id)


def create_active_live(
    user_id: int, live_id: int, live_master_id: int, party_id: int
) -> ExecutableQuery:
    return ExecutableQuery(
        'INSERT INTO "active_live" ("userId", "id", "liveMasterId", "partyId") '
        "VALUES ($1, $2, $3, $4)",
        user_id,
        live_id,
        live_master_id,
        party_id,
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
    clear_lamp: int,
    rate_grade: int,
) -> ExecutableQuery:
    # best-of merge is decided by the caller; this just writes the row for (userId, liveMasterId)
    return ExecutableQuery(
        'UPDATE "live" SET "timesCompleted" = $3, "achievementRate" = $4, '
        '"clearLamp" = $5, "rateGrade" = $6 '
        'WHERE "userId" = $1 AND "liveMasterId" = $2',
        user_id,
        live_master_id,
        times_completed,
        achievement_rate,
        clear_lamp,
        rate_grade,
    )
