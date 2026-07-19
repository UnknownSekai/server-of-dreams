from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from db.friends import (
    add_block,
    remove_block,
    remove_friend,
    remove_request,
    set_friend_favorite,
)
from helpers.friends import (
    accept_request,
    block_list_result,
    list_result,
    resolve_user_id,
    search,
    send_request,
)
from helpers.msgpack import read_request, respond
from helpers.user_data import current_user_id
from models import *

router = APIRouter(tags=["Friends"])


# /api/Friends/AcceptRequest?fromUserId=
@router.post("/api/Friends/AcceptRequest", name="Friends_AcceptFriendRequest")
async def friends_accept_friend_request(
    request: Request, fromUserId: Optional[str] = None
):
    app: YumeApp = request.app
    status = await accept_request(app, current_user_id(request), fromUserId)
    return respond(FriendAcceptResult(result_status=status))


# /api/Friends/BlockUser?targetUserId=
@router.post("/api/Friends/BlockUser", name="Friends_BlockUser")
async def friends_block_user(request: Request, targetUserId: Optional[str] = None):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    if user_id is not None:
        async with app.acquire_db() as conn:
            target = await resolve_user_id(conn, targetUserId)
            if target is not None:
                await conn.execute(add_block(user_id, target))
    return respond(BooleanResult(is_success=True))


# /api/Friends/BlockUsers
@router.get("/api/Friends/BlockUsers", name="Friends_BlockUsers")
async def friends_block_users(request: Request):
    app: YumeApp = request.app
    return respond(await block_list_result(app, current_user_id(request)))


# /api/Friends/CancelRequest?targetUserId=
@router.post("/api/Friends/CancelRequest", name="Friends_CancelFriendRequest")
async def friends_cancel_friend_request(
    request: Request, targetUserId: Optional[str] = None
):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    if user_id is not None:
        async with app.acquire_db() as conn:
            target = await resolve_user_id(conn, targetUserId)
            if target is not None:
                await conn.execute(
                    remove_request(user_id, target)
                )  # my outgoing request
    return respond(BooleanResult(is_success=True))


# /api/Friends/DenyRequest?fromUserId=
@router.post("/api/Friends/DenyRequest", name="Friends_DenyFriendRequest")
async def friends_deny_friend_request(
    request: Request, fromUserId: Optional[str] = None
):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    if user_id is not None:
        async with app.acquire_db() as conn:
            from_id = await resolve_user_id(conn, fromUserId)
            if from_id is not None:
                await conn.execute(
                    remove_request(from_id, user_id)
                )  # their incoming request
    return respond(BooleanResult(is_success=True))


# /api/Friends
@router.get("/api/Friends", name="Friends_GetFriends")
async def friends_get_friends(request: Request):
    app: YumeApp = request.app
    return respond(await list_result(app, current_user_id(request), "friends"))


# /api/ReceivedRequest
@router.post("/api/ReceivedRequest", name="Friends_GetReceivedRequest")
async def friends_get_received_request(request: Request):
    app: YumeApp = request.app
    return respond(await list_result(app, current_user_id(request), "received"))


# /api/SendingRequest
@router.get("/api/SendingRequest", name="Friends_GetSendingRequest")
async def friends_get_sending_request(request: Request):
    app: YumeApp = request.app
    return respond(await list_result(app, current_user_id(request), "sending"))


# /api/Friends/RemoveBlockUser?targetUserId=
@router.post("/api/Friends/RemoveBlockUser", name="Friends_RemoveBlockUser")
async def friends_remove_block_user(
    request: Request, targetUserId: Optional[str] = None
):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    if user_id is not None:
        async with app.acquire_db() as conn:
            target = await resolve_user_id(conn, targetUserId)
            if target is not None:
                await conn.execute(remove_block(user_id, target))
    return respond(BooleanResult(is_success=True))


# /api/Friends/RemoveFriend?targetUserId=
@router.post("/api/Friends/RemoveFriend", name="Friends_RemoveFriend")
async def friends_remove_friend(request: Request, targetUserId: Optional[str] = None):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    if user_id is not None:
        async with app.acquire_db() as conn:  # friendship is two rows, drop both
            target = await resolve_user_id(conn, targetUserId)
            if target is not None:
                await conn.execute(remove_friend(user_id, target))
                await conn.execute(remove_friend(target, user_id))
    return respond(BooleanResult(is_success=True))


# /api/Friends/Search?targetUserId=
@router.post("/api/Friends/Search", name="Friends_SearchFriend")
async def friends_search_friend(request: Request, targetUserId: Optional[str] = None):
    app: YumeApp = request.app
    return respond(await search(app, current_user_id(request), targetUserId))


# /api/Friends/SendRequest?targetUserId=
@router.post("/api/Friends/SendRequest", name="Friends_SendFriendRequest")
async def friends_send_friend_request(
    request: Request, targetUserId: Optional[str] = None
):
    app: YumeApp = request.app
    status = await send_request(app, current_user_id(request), targetUserId)
    return respond(FriendRequestResult(result_status=status))


# /api/Friends/SetFavorite
@router.post("/api/Friends/SetFavorite", name="Friends_SetFriendFavorite")
async def friends_set_friend_favorite(request: Request):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payload = await read_request(request, FriendFavoritePayload)
    if user_id is not None and payload is not None:
        async with app.acquire_db() as conn:
            target = await resolve_user_id(conn, payload.target_user_id)
            if target is not None:
                await conn.execute(
                    set_friend_favorite(user_id, target, payload.set_favorite)
                )
    return respond(BooleanResult(is_success=True))
