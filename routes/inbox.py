import time
from typing import Iterable

from fastapi import APIRouter, Request
from core import YumeApp

from db.user import (
    get_inboxes_by_ids,
    get_unchecked_inboxs,
    mark_inboxs_checked,
    receive_inbox,
)
from helpers.msgpack import read_request, respond
from helpers.things import grant_thing, present_type
from helpers.user_data import build_present, current_user_id, data_object
from models import *

router = APIRouter(tags=["Inbox"])

_MICRO = 1_000_000


async def _receive(app: YumeApp, user_id, inbox_ids: Iterable[int]):
    inbox_ids = list(inbox_ids)
    result = InboxReceiveResult(received_things=[], has_not_receive_things=False)
    if user_id is None or not inbox_ids:
        return respond(result)
    now = int(time.time() * _MICRO)
    received, present_types, received_ids = [], set(), []
    async with app.acquire_db() as conn:
        by_id = {
            r.id: r for r in await conn.fetch(get_inboxes_by_ids(user_id, inbox_ids))
        }
        for inbox_id in inbox_ids:
            row = by_id.get(inbox_id)
            if row is None or row.hasReceived:
                continue  # missing or already claimed
            if row.receiveLimitAt and row.receiveLimitAt < now:
                result.has_not_receive_things = True  # expired -> left unclaimed
                continue
            received.append(
                await grant_thing(
                    conn, user_id, row.thingType, row.thingId, row.thingQuantity
                )
            )
            await conn.execute(receive_inbox(user_id, row.id, now))
            received_ids.append(row.id)
            pt = present_type(row.thingType)
            if pt is not None:
                present_types.add(pt)
    result.received_things = received
    if "Currency" in present_types:  # User mirrors coin/freeJewel/paidJewel
        present_types.add("User")
    # present: the inventory entities the grants wrote + the now-received inbox rows
    updated = [*present_types, ("Inbox", set(received_ids))]
    present = await build_present(app, user_id, *updated)
    return respond(result, present=present)


# /api/Inboxes/BulkReceive
@router.post("/api/Inboxes/BulkReceive", name="Inbox_BulkReceive")
async def inbox_bulk_receive(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, BulkReceivePayload)
    inbox_ids = (
        [int(i) for i in payload.inbox_ids] if payload and payload.inbox_ids else []
    )
    return await _receive(app, current_user_id(request), inbox_ids)


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
    return await _receive(app, current_user_id(request), [inboxId])
