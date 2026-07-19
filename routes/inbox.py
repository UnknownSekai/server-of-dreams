from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from db.user import get_unchecked_inboxs, mark_inboxs_checked
from helpers.msgpack import read_request, respond
from helpers.user_data import current_user_id, data_object
from models import *

router = APIRouter(tags=["Inbox"])


# /api/Inboxes/BulkReceive
@router.post("/api/Inboxes/BulkReceive", name="Inbox_BulkReceive")
async def inbox_bulk_receive(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, BulkReceivePayload)
    return respond(InboxReceiveResult())


# /api/Inboxes/CheckPackagesAsync
@router.post("/api/Inboxes/CheckPackagesAsync", name="Inbox_CheckPackages")
async def inbox_check_packages(request: Request):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    # a diff, not the whole inbox: surface only packages not seen yet, then mark them, so a
    # follow-up call returns an empty present (matching the official).
    present: list = []
    if user_id is not None:
        async with app.acquire_db() as conn:
            rows = await conn.fetch(get_unchecked_inboxs(user_id))
            present = [data_object("Inbox", row) for row in rows]
            if rows:
                await conn.execute(mark_inboxs_checked(user_id))
    return respond(BooleanResult(is_success=True), present=present)


# /api/Inboxes/{inboxId}/Receive
@router.post("/api/Inboxes/{inboxId}/Receive", name="Inbox_Receive")
async def inbox_receive(request: Request, inboxId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(InboxReceiveResult())
