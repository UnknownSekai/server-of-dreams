from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from helpers.auth import login
from models import *

router = APIRouter(prefix="/api/Login", tags=["Login"])


# /api/Login
@router.post("/", name="Login_Login")
async def login_login(request: Request):
    payload = await read_request(request, "LoginPayload")
    return respond(login(payload))
