from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/Friends", tags=["Friends"])


# /api/Friends
@router.get("/", name="Friends_GetFriends")
async def friends_get_friends(request: Request):
    return respond(FriendListResult())


# /api/Friends/AcceptRequest?fromUserId=
@router.post("/AcceptRequest", name="Friends_AcceptFriendRequest")
async def friends_accept_friend_request(request: Request):
    return respond(FriendAcceptResult())


# /api/Friends/BlockUser?targetUserId=
@router.post("/BlockUser", name="Friends_BlockUser")
async def friends_block_user(request: Request):
    return respond(BooleanResult())


# /api/Friends/BlockUsers
@router.get("/BlockUsers", name="Friends_BlockUsers")
async def friends_block_users(request: Request):
    return respond(BlockListResult())


# /api/Friends/CancelRequest?targetUserId=
@router.post("/CancelRequest", name="Friends_CancelFriendRequest")
async def friends_cancel_friend_request(request: Request):
    return respond(BooleanResult())


# /api/Friends/DenyRequest?fromUserId=
@router.post("/DenyRequest", name="Friends_DenyFriendRequest")
async def friends_deny_friend_request(request: Request):
    return respond(BooleanResult())


# /api/Friends/RemoveBlockUser?targetUserId=
@router.post("/RemoveBlockUser", name="Friends_RemoveBlockUser")
async def friends_remove_block_user(request: Request):
    return respond(BooleanResult())


# /api/Friends/RemoveFriend?targetUserId=
@router.post("/RemoveFriend", name="Friends_RemoveFriend")
async def friends_remove_friend(request: Request):
    return respond(BooleanResult())


# /api/Friends/Search?targetUserId=
@router.post("/Search", name="Friends_SearchFriend")
async def friends_search_friend(request: Request):
    return respond(FriendSearchResult())


# /api/Friends/SendRequest?targetUserId=
@router.post("/SendRequest", name="Friends_SendFriendRequest")
async def friends_send_friend_request(request: Request):
    return respond(FriendRequestResult())


# /api/Friends/SetFavorite
@router.post("/SetFavorite", name="Friends_SetFriendFavorite")
async def friends_set_friend_favorite(request: Request):
    payload = await read_request(request, "FriendFavoritePayload")
    return respond(BooleanResult())
