from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/FriendInvitation", tags=["FriendInvitation"])


# /api/FriendInvitation/Check?invitationCode=
@router.get("/Check", name="FriendInvitation_CheckInvitationCodeInfo")
async def friend_invitation_check_invitation_code_info(request: Request):
    return respond(FriendInvitationUserInfoResult())


# /api/FriendInvitation/Input?invitationCode=
@router.post("/Input", name="FriendInvitation_ActivateInvitationCode")
async def friend_invitation_activate_invitation_code(request: Request):
    return respond(BooleanResult())


# /api/FriendInvitation/Receive
@router.post("/Receive", name="FriendInvitation_ReceiveInvitationMissionRewards")
async def friend_invitation_receive_invitation_mission_rewards(request: Request):
    payload = await read_request(request, "FriendInvitationMissionPayload")
    return respond([])


# /api/FriendInvitation/Update
@router.post("/Update", name="FriendInvitation_UpdateInvitationMission")
async def friend_invitation_update_invitation_mission(request: Request):
    return respond(BooleanResult())
