from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/MultiRooms", tags=["MultiRooms"])


# /api/MultiRooms
@router.get("/", name="MultiRoom_GetMultiRooms")
async def multi_room_get_multi_rooms(request: Request):
    return respond([])


# /api/MultiRooms/Create
@router.post("/Create", name="MultiRoom_CreateMultiRooms")
async def multi_room_create_multi_rooms(request: Request):
    payload = await read_request(request, "CreateMultiRoomPayload")
    return respond(MultiRoomCreateResult())


# /api/MultiRooms/Detail?hashedMultiRoomId=
@router.post("/Detail", name="MultiRoom_GetMultiRoomDetail")
async def multi_room_get_multi_room_detail(request: Request):
    return respond(MultiRoomDetailResult())


# /api/MultiRooms/Invited
@router.post("/Invited", name="MultiRoom_GetInvitedMultiRooms")
async def multi_room_get_invited_multi_rooms(request: Request):
    return respond([])


# /api/MultiRooms/Join
@router.post("/Join", name="MultiRoom_JoinMultiRooms")
async def multi_room_join_multi_rooms(request: Request):
    payload = await read_request(request, "JoinMultiRoomPayload")
    return respond(BooleanResult())


# /api/MultiRooms/Joined
@router.post("/Joined", name="MultiRoom_GetJoinedMultiRooms")
async def multi_room_get_joined_multi_rooms(request: Request):
    return respond([])


# /api/MultiRooms/Release?hashedMultiRoomId=
@router.post("/Release", name="MultiRoom_ReleaseMultiRooms")
async def multi_room_release_multi_rooms(request: Request):
    return respond(BooleanResult())


# /api/MultiRooms/Resignation?hashedMultiRoomId=
@router.post("/Resignation", name="MultiRoom_ResignationMultiRoom")
async def multi_room_resignation_multi_room(request: Request):
    return respond(BooleanResult())


# /api/MultiRooms/Send/Invite
@router.post("/Send/Invite", name="MultiRoom_SendMultiRoomInvite")
async def multi_room_send_multi_room_invite(request: Request):
    payload = await read_request(request, "InviteMultiRoomPayload")
    return respond(BooleanResult())
