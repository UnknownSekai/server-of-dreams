from db.query import ExecutableQuery


def create_account(
    user_id: int,
    credential: str,
    platform: str = "Android",
    registered_at: int = 0,
    last_login_at: int = 0,
) -> ExecutableQuery:
    return ExecutableQuery(
        'INSERT INTO "accounts" '
        '("userId", "credential", "platform", "registeredAt", "lastLoginAt") '
        "VALUES ($1, $2, $3, $4, $5) "
        'ON CONFLICT ("userId") DO NOTHING',
        user_id,
        credential,
        platform,
        registered_at,
        last_login_at,
    )


def add_hash_user_id(hash_user_id: str, user_id: int) -> ExecutableQuery:
    return ExecutableQuery(
        'INSERT INTO "hash_user_id" ("hashUserId", "userId") VALUES ($1, $2) '
        'ON CONFLICT ("hashUserId") DO NOTHING',
        hash_user_id,
        user_id,
    )


def update_account_token(user_id: int, api_token: str) -> ExecutableQuery:
    return ExecutableQuery(
        'UPDATE "accounts" SET "apiToken" = $1 WHERE "userId" = $2',
        api_token,
        user_id,
    )


def update_last_login(user_id: int, last_login_at: int) -> ExecutableQuery:
    return ExecutableQuery(
        'UPDATE "accounts" SET "lastLoginAt" = $1 WHERE "userId" = $2',
        last_login_at,
        user_id,
    )
