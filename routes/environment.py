from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.config import config
from helpers.environment import environment
from helpers.msgpack import respond
from models import *

router = APIRouter(tags=["Environment"])


# /api/Environment?applicationVersion=&gameVersion=
@router.post("/api/Environment", name="Environment_GetEnvironment")
async def environment_get_environment(
    request: Request,
    applicationVersion: Optional[str] = None,
    gameVersion: Optional[int] = None,
):
    app: YumeApp = request.app
    if applicationVersion != str(config["server_version"]):
        return respond(EnvironmentResult())
    return respond(environment())


# /api/Environment/Ping
@router.get("/api/Environment/Ping", name="Environment_Ping")
async def environment_ping(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())
