from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import read_request, respond
from helpers.auth import login
from models import *

router = APIRouter(tags=["Login"])


# /api/Login
@router.post("/api/Login", name="Login_Login")
async def login_login(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "LoginPayload")
    return respond(login(payload))
