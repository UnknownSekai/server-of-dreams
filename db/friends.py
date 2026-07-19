"""Queries for the friend system: friendships (one row per direction), pending requests
(from -> to), and blocks (reusing the user_block table)."""

from db.query import ExecutableQuery, SelectQuery
from models.database import FriendModel, FriendRequestModel, UserBlockModel

# -- friendships ---------------------------------------------------------------


def get_friends(user_id: int) -> SelectQuery[FriendModel]:
    return SelectQuery(
        FriendModel,
        'SELECT * FROM "friend" WHERE "userId" = $1 ORDER BY "isFavorite" DESC, "createdAt"',
        user_id,
    )


def get_friend(user_id: int, friend_user_id: int) -> SelectQuery[FriendModel]:
    return SelectQuery(
        FriendModel,
        'SELECT * FROM "friend" WHERE "userId" = $1 AND "friendUserId" = $2',
        user_id,
        friend_user_id,
    )


def add_friend(user_id: int, friend_user_id: int, now: int) -> ExecutableQuery:
    return ExecutableQuery(
        'INSERT INTO "friend" ("userId", "friendUserId", "isFavorite", "createdAt") '
        "VALUES ($1, $2, false, $3) "
        'ON CONFLICT ("userId", "friendUserId") DO NOTHING',
        user_id,
        friend_user_id,
        now,
    )


def remove_friend(user_id: int, friend_user_id: int) -> ExecutableQuery:
    return ExecutableQuery(
        'DELETE FROM "friend" WHERE "userId" = $1 AND "friendUserId" = $2',
        user_id,
        friend_user_id,
    )


def set_friend_favorite(
    user_id: int, friend_user_id: int, favorite: bool
) -> ExecutableQuery:
    return ExecutableQuery(
        'UPDATE "friend" SET "isFavorite" = $3 WHERE "userId" = $1 AND "friendUserId" = $2',
        user_id,
        friend_user_id,
        favorite,
    )


# -- requests ------------------------------------------------------------------


def get_received_requests(user_id: int) -> SelectQuery[FriendRequestModel]:
    return SelectQuery(
        FriendRequestModel,
        'SELECT * FROM "friend_request" WHERE "toUserId" = $1 ORDER BY "createdAt"',
        user_id,
    )


def get_sending_requests(user_id: int) -> SelectQuery[FriendRequestModel]:
    return SelectQuery(
        FriendRequestModel,
        'SELECT * FROM "friend_request" WHERE "fromUserId" = $1 ORDER BY "createdAt"',
        user_id,
    )


def get_request(from_user_id: int, to_user_id: int) -> SelectQuery[FriendRequestModel]:
    return SelectQuery(
        FriendRequestModel,
        'SELECT * FROM "friend_request" WHERE "fromUserId" = $1 AND "toUserId" = $2',
        from_user_id,
        to_user_id,
    )


def add_request(from_user_id: int, to_user_id: int, now: int) -> ExecutableQuery:
    return ExecutableQuery(
        'INSERT INTO "friend_request" ("fromUserId", "toUserId", "createdAt") '
        "VALUES ($1, $2, $3) "
        'ON CONFLICT ("fromUserId", "toUserId") DO NOTHING',
        from_user_id,
        to_user_id,
        now,
    )


def remove_request(from_user_id: int, to_user_id: int) -> ExecutableQuery:
    return ExecutableQuery(
        'DELETE FROM "friend_request" WHERE "fromUserId" = $1 AND "toUserId" = $2',
        from_user_id,
        to_user_id,
    )


# -- blocks (user_block table) -------------------------------------------------


def get_blocks(user_id: int) -> SelectQuery[UserBlockModel]:
    return SelectQuery(
        UserBlockModel, 'SELECT * FROM "user_block" WHERE "userId" = $1', user_id
    )


def add_block(user_id: int, block_user_id: int) -> ExecutableQuery:
    return ExecutableQuery(
        'INSERT INTO "user_block" ("userId", "id", "blockUserId") VALUES ($1, $2, $3)',
        user_id,
        block_user_id,
        str(block_user_id),
    )


def remove_block(user_id: int, block_user_id: int) -> ExecutableQuery:
    return ExecutableQuery(
        'DELETE FROM "user_block" WHERE "userId" = $1 AND "blockUserId" = $2',
        user_id,
        str(block_user_id),
    )
