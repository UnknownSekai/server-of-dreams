from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/SendingRequest", tags=["SendingRequest"])


# /api/SendingRequest
@router.get("/", name="Friends_GetSendingRequest")
async def friends_get_sending_request(request: Request):
    return respond(FriendListResult())
