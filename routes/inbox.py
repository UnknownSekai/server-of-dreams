from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import raw_response, read_request, respond
from models import *

router = APIRouter(tags=["Inbox"])


# /api/Inboxes/BulkReceive
@router.post("/api/Inboxes/BulkReceive", name="Inbox_BulkReceive")
async def inbox_bulk_receive(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "BulkReceivePayload")
    return respond(InboxReceiveResult())


# /api/Inboxes/CheckPackagesAsync
@router.post("/api/Inboxes/CheckPackagesAsync", name="Inbox_CheckPackages")
async def inbox_check_packages(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Inboxes/{inboxId}/Receive
@router.post("/api/Inboxes/{inboxId}/Receive", name="Inbox_Receive")
async def inbox_receive(request: Request, inboxId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(InboxReceiveResult())
