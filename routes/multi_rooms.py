from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/MultiRooms", tags=["MultiRooms"])


# /api/MultiRooms
@router.get(
    "/", response_model=list[MultiRoomInformationResult], name="MultiRoom_GetMultiRooms"
)
async def multi_room_get_multi_rooms() -> list[MultiRoomInformationResult]:
    return []


# /api/MultiRooms/Create
@router.post(
    "/Create", response_model=MultiRoomCreateResult, name="MultiRoom_CreateMultiRooms"
)
async def multi_room_create_multi_rooms(
    body: CreateMultiRoomPayload,
) -> MultiRoomCreateResult:
    return MultiRoomCreateResult()


# /api/MultiRooms/Detail?hashedMultiRoomId=
@router.post(
    "/Detail", response_model=MultiRoomDetailResult, name="MultiRoom_GetMultiRoomDetail"
)
async def multi_room_get_multi_room_detail(
    hashedMultiRoomId: str,
) -> MultiRoomDetailResult:
    return MultiRoomDetailResult()


# /api/MultiRooms/Invited
@router.post(
    "/Invited",
    response_model=list[MultiRoomInvitedResult],
    name="MultiRoom_GetInvitedMultiRooms",
)
async def multi_room_get_invited_multi_rooms() -> list[MultiRoomInvitedResult]:
    return []


# /api/MultiRooms/Join
@router.post("/Join", response_model=BooleanResult, name="MultiRoom_JoinMultiRooms")
async def multi_room_join_multi_rooms(body: JoinMultiRoomPayload) -> BooleanResult:
    return BooleanResult()


# /api/MultiRooms/Joined
@router.post(
    "/Joined",
    response_model=list[MultiRoomJoinnedResult],
    name="MultiRoom_GetJoinedMultiRooms",
)
async def multi_room_get_joined_multi_rooms() -> list[MultiRoomJoinnedResult]:
    return []


# /api/MultiRooms/Release?hashedMultiRoomId=
@router.post(
    "/Release", response_model=BooleanResult, name="MultiRoom_ReleaseMultiRooms"
)
async def multi_room_release_multi_rooms(hashedMultiRoomId: str) -> BooleanResult:
    return BooleanResult()


# /api/MultiRooms/Resignation?hashedMultiRoomId=
@router.post(
    "/Resignation", response_model=BooleanResult, name="MultiRoom_ResignationMultiRoom"
)
async def multi_room_resignation_multi_room(hashedMultiRoomId: str) -> BooleanResult:
    return BooleanResult()


# /api/MultiRooms/Send/Invite
@router.post(
    "/Send/Invite", response_model=BooleanResult, name="MultiRoom_SendMultiRoomInvite"
)
async def multi_room_send_multi_room_invite(
    body: InviteMultiRoomPayload,
) -> BooleanResult:
    return BooleanResult()
