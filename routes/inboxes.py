from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/Inboxes", tags=["Inboxes"])


# /api/Inboxes/BulkReceive
@router.post(
    "/BulkReceive", response_model=InboxReceiveResult, name="Inbox_BulkReceive"
)
async def inbox_bulk_receive(body: BulkReceivePayload) -> InboxReceiveResult:
    return InboxReceiveResult()


# /api/Inboxes/CheckPackagesAsync
@router.post(
    "/CheckPackagesAsync", response_model=BooleanResult, name="Inbox_CheckPackages"
)
async def inbox_check_packages() -> BooleanResult:
    return BooleanResult()
