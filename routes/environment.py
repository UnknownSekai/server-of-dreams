from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import raw_response, read_request, respond
from models import *

router = APIRouter(tags=["Environment"])


# /api/Environment/GetEnvironment?applicationVersion=&gameVersion=
@router.post("/api/Environment/GetEnvironment", name="Environment_GetEnvironment")
async def environment_get_environment(
    request: Request,
    applicationVersion: Optional[str] = None,
    gameVersion: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(EnvironmentResult())


# /api/Environment/Ping
@router.get("/api/Environment/Ping", name="Environment_Ping")
async def environment_ping(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())
