from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/Inboxes", tags=["Inboxes"])


# /api/Inboxes/BulkReceive
@router.post("/BulkReceive", name="Inbox_BulkReceive")
async def inbox_bulk_receive(request: Request):
    payload = await read_request(request, "BulkReceivePayload")
    return respond(InboxReceiveResult())


# /api/Inboxes/CheckPackagesAsync
@router.post("/CheckPackagesAsync", name="Inbox_CheckPackages")
async def inbox_check_packages(request: Request):
    return respond(BooleanResult())
