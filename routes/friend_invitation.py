from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(tags=["FriendInvitation"])


# /api/FriendInvitation/Input?invitationCode=
@router.post(
    "/api/FriendInvitation/Input", name="FriendInvitation_ActivateInvitationCode"
)
async def friend_invitation_activate_invitation_code(
    request: Request, invitationCode: Optional[str] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/FriendInvitation/Check?invitationCode=
@router.get(
    "/api/FriendInvitation/Check", name="FriendInvitation_CheckInvitationCodeInfo"
)
async def friend_invitation_check_invitation_code_info(
    request: Request, invitationCode: Optional[str] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(FriendInvitationUserInfoResult())


# /api/FriendInvitation/Receive
@router.post(
    "/api/FriendInvitation/Receive",
    name="FriendInvitation_ReceiveInvitationMissionRewards",
)
async def friend_invitation_receive_invitation_mission_rewards(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, FriendInvitationMissionPayload)
    return respond([ReceivedThing()])


# /api/FriendInvitation/Update
@router.post(
    "/api/FriendInvitation/Update", name="FriendInvitation_UpdateInvitationMission"
)
async def friend_invitation_update_invitation_mission(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())
