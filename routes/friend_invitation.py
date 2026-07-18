from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/FriendInvitation", tags=["FriendInvitation"])


# /api/FriendInvitation/Check?invitationCode=
@router.get(
    "/Check",
    response_model=FriendInvitationUserInfoResult,
    name="FriendInvitation_CheckInvitationCodeInfo",
)
async def friend_invitation_check_invitation_code_info(
    invitationCode: str,
) -> FriendInvitationUserInfoResult:
    return FriendInvitationUserInfoResult()


# /api/FriendInvitation/Input?invitationCode=
@router.post(
    "/Input",
    response_model=BooleanResult,
    name="FriendInvitation_ActivateInvitationCode",
)
async def friend_invitation_activate_invitation_code(
    invitationCode: str,
) -> BooleanResult:
    return BooleanResult()


# /api/FriendInvitation/Receive
@router.post(
    "/Receive",
    response_model=list[ReceivedThing],
    name="FriendInvitation_ReceiveInvitationMissionRewards",
)
async def friend_invitation_receive_invitation_mission_rewards(
    body: FriendInvitationMissionPayload,
) -> list[ReceivedThing]:
    return []


# /api/FriendInvitation/Update
@router.post(
    "/Update",
    response_model=BooleanResult,
    name="FriendInvitation_UpdateInvitationMission",
)
async def friend_invitation_update_invitation_mission() -> BooleanResult:
    return BooleanResult()
