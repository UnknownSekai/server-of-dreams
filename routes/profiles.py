from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/Profiles", tags=["Profiles"])


# /api/Profiles/Edit
@router.post("/Edit", name="Profile_Edit")
async def profile_edit(request: Request):
    payload = await read_request(request, "EditUserProfilePayload")
    return respond(BooleanResult())
