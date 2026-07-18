from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(tags=["Friends"])


# /api/Friends/AcceptRequest?fromUserId=
@router.post("/api/Friends/AcceptRequest", name="Friends_AcceptFriendRequest")
async def friends_accept_friend_request(
    request: Request, fromUserId: Optional[str] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(FriendAcceptResult())


# /api/Friends/BlockUser?targetUserId=?targetUserId=
@router.post("/api/Friends/BlockUser?targetUserId=", name="Friends_BlockUser")
async def friends_block_user(request: Request, targetUserId: Optional[str] = None):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Friends/BlockUsers
@router.get("/api/Friends/BlockUsers", name="Friends_BlockUsers")
async def friends_block_users(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BlockListResult())


# /api/Friends/CancelRequest?targetUserId=
@router.post("/api/Friends/CancelRequest", name="Friends_CancelFriendRequest")
async def friends_cancel_friend_request(
    request: Request, targetUserId: Optional[str] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Friends/DenyRequest?fromUserId=
@router.post("/api/Friends/DenyRequest", name="Friends_DenyFriendRequest")
async def friends_deny_friend_request(
    request: Request, fromUserId: Optional[str] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Friends
@router.get("/api/Friends", name="Friends_GetFriends")
async def friends_get_friends(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(FriendListResult())


# /api/ReceivedRequest
@router.post("/api/ReceivedRequest", name="Friends_GetReceivedRequest")
async def friends_get_received_request(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(FriendListResult())


# /api/SendingRequest
@router.get("/api/SendingRequest", name="Friends_GetSendingRequest")
async def friends_get_sending_request(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(FriendListResult())


# /api/Friends/RemoveBlockUser?targetUserId=?targetUserId=
@router.post(
    "/api/Friends/RemoveBlockUser?targetUserId=", name="Friends_RemoveBlockUser"
)
async def friends_remove_block_user(
    request: Request, targetUserId: Optional[str] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Friends/RemoveFriend?targetUserId=
@router.post("/api/Friends/RemoveFriend", name="Friends_RemoveFriend")
async def friends_remove_friend(request: Request, targetUserId: Optional[str] = None):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Friends/Search?targetUserId=
@router.post("/api/Friends/Search", name="Friends_SearchFriend")
async def friends_search_friend(request: Request, targetUserId: Optional[str] = None):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(FriendSearchResult())


# /api/Friends/SendRequest?targetUserId=
@router.post("/api/Friends/SendRequest", name="Friends_SendFriendRequest")
async def friends_send_friend_request(
    request: Request, targetUserId: Optional[str] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(FriendRequestResult())


# /api/Friends/SetFavorite
@router.post("/api/Friends/SetFavorite", name="Friends_SetFriendFavorite")
async def friends_set_friend_favorite(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "FriendFavoritePayload")
    return respond(BooleanResult())
