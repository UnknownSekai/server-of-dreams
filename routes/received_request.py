from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/ReceivedRequest", tags=["ReceivedRequest"])


# /api/ReceivedRequest
@router.post("/", name="Friends_GetReceivedRequest")
async def friends_get_received_request(request: Request):
    return respond(FriendListResult())
