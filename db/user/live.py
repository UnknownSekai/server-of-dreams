from db.query import ExecutableQuery


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
