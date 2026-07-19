import datetime
import time
from typing import Optional

from db.account import get_account_by_id, get_user_id_by_hash
from db.friends import (
    add_friend,
    add_request,
    get_blocks,
    get_friend,
    get_friends,
    get_received_requests,
    get_request,
    get_sending_requests,
    remove_request,
)
from db.user import get_user_profiles, get_users
from helpers.user_hash import hash_id
from models import (
    BlockListResult,
    FriendAcceptResultStatus,
    FriendListResult,
    FriendRequestResultStatus,
    FriendResult,
    FriendSearchResult,
    FriendSearchResultStatus,
)

_FRIEND_LIMIT = 200


async def resolve_user_id(conn, value: Optional[str]) -> Optional[int]:
    """Map a client-supplied hashUserId string to its sequential userId via the lookup table."""
    if value is None:
        return None
    row = await conn.fetchrow(get_user_id_by_hash(value))
    return row.userId if row is not None else None


def _now() -> int:
    return int(time.time() * 1_000_000)


def _iso(seconds: int) -> str:
    return datetime.datetime.fromtimestamp(
        seconds or 0, datetime.timezone.utc
    ).isoformat()


async def _friend_result(
    conn, target_id: int, is_favorite: bool
) -> Optional[FriendResult]:
    """Project another user's User + UserProfile (+ account.lastLoginAt) into a FriendResult."""
    user = await conn.fetchrow(get_users(target_id))
    profile = await conn.fetchrow(get_user_profiles(target_id))
    if user is None or profile is None:
        return None
    account = await conn.fetchrow(get_account_by_id(target_id))
    return FriendResult(
        user_id=user.hashUserId or hash_id(target_id),
        player_rank=user.playerRank,
        trophy_master_id1=profile.mTrophyId1 or 0,
        trophy_master_id2=profile.mTrophyId2 or 0,
        trophy_master_id3=profile.mTrophyId3 or 0,
        introduction=profile.introduction,
        last_logged_in_at=_iso(account.lastLoginAt if account else 0),
        name=profile.name,
        player_rate=profile.playerRate,
        is_public_player_rate=profile.isPublicPlayerRate,
        league_class=profile.leagueClass,
        character_ranks=[],  # TODO: populate from the target's character star ranks
        is_public_album_main_page=profile.isPublicAlbumMainPage,
        main_character_master_id=profile.mainCharacterMasterId,
        display_awakening_status=profile.displayAwakeningStatus,
        icon_frame_master_id=profile.iconFrameMasterId,
        is_favorite=is_favorite,
    )


async def list_result(app, user_id: Optional[int], kind: str) -> FriendListResult:
    """FriendListResult for kind in {friends, received, sending}. current_friend_count is
    always the real friend count regardless of which list is requested."""
    if user_id is None:
        return FriendListResult(results=[], current_friend_count=0)
    async with app.acquire_db() as conn:
        friends = await conn.fetch(get_friends(user_id))
        if kind == "friends":
            targets = [(f.friendUserId, f.isFavorite) for f in friends]
        elif kind == "received":
            reqs = await conn.fetch(get_received_requests(user_id))
            targets = [(r.fromUserId, False) for r in reqs]
        else:  # sending
            reqs = await conn.fetch(get_sending_requests(user_id))
            targets = [(r.toUserId, False) for r in reqs]
        results = []
        for target_id, favorite in targets:
            fr = await _friend_result(conn, target_id, favorite)
            if fr is not None:
                results.append(fr)
    return FriendListResult(results=results, current_friend_count=len(friends))


async def block_list_result(app, user_id: Optional[int]) -> BlockListResult:
    if user_id is None:
        return BlockListResult(results=[])
    async with app.acquire_db() as conn:
        results = []
        for block in await conn.fetch(get_blocks(user_id)):
            try:
                target_id = (
                    int(block.blockUserId) if block.blockUserId is not None else None
                )
            except (TypeError, ValueError):
                target_id = None
            if target_id is not None:
                fr = await _friend_result(conn, target_id, False)
                if fr is not None:
                    results.append(fr)
    return BlockListResult(results=results)


async def send_request(app, user_id: Optional[int], target_str: Optional[str]) -> int:
    S = FriendRequestResultStatus
    if user_id is None:
        return S.DataNotFound
    async with app.acquire_db() as conn:
        target = await resolve_user_id(conn, target_str)
        if target is None:
            return S.DataNotFound
        if target == user_id:
            return S.IsMySelf
        if await conn.fetchrow(get_users(target)) is None:
            return S.DataNotFound
        if await conn.fetchrow(get_friend(user_id, target)) is not None:
            return S.IsFriends
        if await conn.fetchrow(get_request(user_id, target)) is not None:
            return S.IsApplying
        # mutual: they already requested us -> becoming friends instead of re-requesting
        if await conn.fetchrow(get_request(target, user_id)) is not None:
            now = _now()
            await conn.execute(remove_request(target, user_id))
            await conn.execute(add_friend(user_id, target, now))
            await conn.execute(add_friend(target, user_id, now))
            return S.RequestSuccess
        if len(await conn.fetch(get_friends(user_id))) >= _FRIEND_LIMIT:
            return S.IsFriendCountLimit
        await conn.execute(add_request(user_id, target, _now()))
    return S.RequestSuccess


async def accept_request(app, user_id: Optional[int], from_str: Optional[str]) -> int:
    S = FriendAcceptResultStatus
    if user_id is None:
        return S.Canceled
    async with app.acquire_db() as conn:
        from_id = await resolve_user_id(conn, from_str)
        if from_id is None:
            return S.Canceled
        if await conn.fetchrow(get_request(from_id, user_id)) is None:
            return S.Canceled  # request was cancelled / never existed
        if len(await conn.fetch(get_friends(user_id))) >= _FRIEND_LIMIT:
            return S.AcceptUserFriendsLimitOver
        if len(await conn.fetch(get_friends(from_id))) >= _FRIEND_LIMIT:
            return S.RequestUserFriendsLimitOver
        now = _now()
        await conn.execute(remove_request(from_id, user_id))
        await conn.execute(add_friend(user_id, from_id, now))
        await conn.execute(add_friend(from_id, user_id, now))
    return S.AcceptSuccess


async def search(
    app, user_id: Optional[int], target_str: Optional[str]
) -> FriendSearchResult:
    S = FriendSearchResultStatus
    if user_id is None:
        return FriendSearchResult(friend_result=None, result_status=S.None_)
    async with app.acquire_db() as conn:
        target = await resolve_user_id(conn, target_str)
        if target is None:
            return FriendSearchResult(friend_result=None, result_status=S.None_)
        if await conn.fetchrow(get_users(target)) is None:
            return FriendSearchResult(friend_result=None, result_status=S.None_)
        friend = await conn.fetchrow(get_friend(user_id, target))
        if friend is not None:
            status = S.Friend
        elif await conn.fetchrow(get_request(user_id, target)) is not None:
            status = S.Request
        elif await conn.fetchrow(get_request(target, user_id)) is not None:
            status = S.ReceivedRequest
        else:
            status = S.User
        fr = await _friend_result(conn, target, friend.isFavorite if friend else False)
    return FriendSearchResult(friend_result=fr, result_status=status)
