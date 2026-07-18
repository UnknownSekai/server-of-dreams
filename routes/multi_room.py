from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import raw_response, read_request, respond
from models import *

router = APIRouter(tags=["MultiRoom"])


# /api/MultiRooms/Create
@router.post("/api/MultiRooms/Create", name="MultiRoom_CreateMultiRooms")
async def multi_room_create_multi_rooms(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "CreateMultiRoomPayload")
    return respond(MultiRoomCreateResult())


# /api/MultiRooms/Invited
@router.post("/api/MultiRooms/Invited", name="MultiRoom_GetInvitedMultiRooms")
async def multi_room_get_invited_multi_rooms(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])


# /api/MultiRooms/Joined
@router.post("/api/MultiRooms/Joined", name="MultiRoom_GetJoinedMultiRooms")
async def multi_room_get_joined_multi_rooms(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])


# /api/MultiRooms/Detail?hashedMultiRoomId=?hashedMultiRoomId=
@router.post(
    "/api/MultiRooms/Detail?hashedMultiRoomId=", name="MultiRoom_GetMultiRoomDetail"
)
async def multi_room_get_multi_room_detail(
    request: Request, hashedMultiRoomId: Optional[str] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(MultiRoomDetailResult())


# /api/MultiRooms
@router.get("/api/MultiRooms", name="MultiRoom_GetMultiRooms")
async def multi_room_get_multi_rooms(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])


# /api/MultiRoom/GetSearchMultiRooms?HashedRoomId=&LiveMasterId=
@router.get("/api/MultiRoom/GetSearchMultiRooms", name="MultiRoom_GetSearchMultiRooms")
async def multi_room_get_search_multi_rooms(
    request: Request,
    HashedRoomId: Optional[str] = None,
    LiveMasterId: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response([])


# /api/MultiRooms/Join
@router.post("/api/MultiRooms/Join", name="MultiRoom_JoinMultiRooms")
async def multi_room_join_multi_rooms(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "JoinMultiRoomPayload")
    return respond(BooleanResult())


# /api/MultiRooms/Release?hashedMultiRoomId=?hashedMultiRoomId=
@router.post(
    "/api/MultiRooms/Release?hashedMultiRoomId=", name="MultiRoom_ReleaseMultiRooms"
)
async def multi_room_release_multi_rooms(
    request: Request, hashedMultiRoomId: Optional[str] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/MultiRooms/Resignation?hashedMultiRoomId=?hashedMultiRoomId=
@router.post(
    "/api/MultiRooms/Resignation?hashedMultiRoomId=",
    name="MultiRoom_ResignationMultiRoom",
)
async def multi_room_resignation_multi_room(
    request: Request, hashedMultiRoomId: Optional[str] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/MultiRooms/Send/Invite
@router.post("/api/MultiRooms/Send/Invite", name="MultiRoom_SendMultiRoomInvite")
async def multi_room_send_multi_room_invite(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "InviteMultiRoomPayload")
    return respond(BooleanResult())
