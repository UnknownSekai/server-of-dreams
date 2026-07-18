from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/Friends", tags=["Friends"])


# /api/Friends
@router.get("/", response_model=FriendListResult, name="Friends_GetFriends")
async def friends_get_friends() -> FriendListResult:
    return FriendListResult()


# /api/Friends/AcceptRequest?fromUserId=
@router.post(
    "/AcceptRequest",
    response_model=FriendAcceptResult,
    name="Friends_AcceptFriendRequest",
)
async def friends_accept_friend_request(fromUserId: str) -> FriendAcceptResult:
    return FriendAcceptResult()


# /api/Friends/BlockUser?targetUserId=
@router.post("/BlockUser", response_model=BooleanResult, name="Friends_BlockUser")
async def friends_block_user(targetUserId: str) -> BooleanResult:
    return BooleanResult()


# /api/Friends/BlockUsers
@router.get("/BlockUsers", response_model=BlockListResult, name="Friends_BlockUsers")
async def friends_block_users() -> BlockListResult:
    return BlockListResult()


# /api/Friends/CancelRequest?targetUserId=
@router.post(
    "/CancelRequest", response_model=BooleanResult, name="Friends_CancelFriendRequest"
)
async def friends_cancel_friend_request(targetUserId: str) -> BooleanResult:
    return BooleanResult()


# /api/Friends/DenyRequest?fromUserId=
@router.post(
    "/DenyRequest", response_model=BooleanResult, name="Friends_DenyFriendRequest"
)
async def friends_deny_friend_request(fromUserId: str) -> BooleanResult:
    return BooleanResult()


# /api/Friends/RemoveBlockUser?targetUserId=
@router.post(
    "/RemoveBlockUser", response_model=BooleanResult, name="Friends_RemoveBlockUser"
)
async def friends_remove_block_user(targetUserId: str) -> BooleanResult:
    return BooleanResult()


# /api/Friends/RemoveFriend?targetUserId=
@router.post("/RemoveFriend", response_model=BooleanResult, name="Friends_RemoveFriend")
async def friends_remove_friend(targetUserId: str) -> BooleanResult:
    return BooleanResult()


# /api/Friends/Search?targetUserId=
@router.post("/Search", response_model=FriendSearchResult, name="Friends_SearchFriend")
async def friends_search_friend(targetUserId: str) -> FriendSearchResult:
    return FriendSearchResult()


# /api/Friends/SendRequest?targetUserId=
@router.post(
    "/SendRequest", response_model=FriendRequestResult, name="Friends_SendFriendRequest"
)
async def friends_send_friend_request(targetUserId: str) -> FriendRequestResult:
    return FriendRequestResult()


# /api/Friends/SetFavorite
@router.post(
    "/SetFavorite", response_model=BooleanResult, name="Friends_SetFriendFavorite"
)
async def friends_set_friend_favorite(body: FriendFavoritePayload) -> BooleanResult:
    return BooleanResult()
