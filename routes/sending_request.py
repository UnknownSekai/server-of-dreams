from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/SendingRequest", tags=["SendingRequest"])


# /api/SendingRequest
@router.get("/", response_model=FriendListResult, name="Friends_GetSendingRequest")
async def friends_get_sending_request() -> FriendListResult:
    return FriendListResult()
