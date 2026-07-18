from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(tags=["Profile"])


# /api/Profiles/Edit
@router.post("/api/Profiles/Edit", name="Profile_Edit")
async def profile_edit(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "EditUserProfilePayload")
    return respond(BooleanResult())
