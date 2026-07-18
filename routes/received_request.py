from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/ReceivedRequest", tags=["ReceivedRequest"])


# /api/ReceivedRequest
@router.post("/", response_model=FriendListResult, name="Friends_GetReceivedRequest")
async def friends_get_received_request() -> FriendListResult:
    return FriendListResult()
