from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/Environment", tags=["Environment"])


# /api/Environment/Ping
@router.get("/Ping", name="Environment_Ping")
async def environment_ping(request: Request):
    return respond(BooleanResult())
