from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import read_request, respond
from helpers.auth import authenticate
from helpers.auth import register
from models import *

router = APIRouter(tags=["Account"])


# /api/Account/Authenticate
@router.post("/api/Account/Authenticate", name="Account_Authenticate")
async def account_authenticate(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, AuthenticatePayload)
    return respond(await authenticate(payload, app))


# /api/Account/ConnectAccount
@router.post("/api/Account/ConnectAccount", name="Account_ConnectAccount")
async def account_connect_account(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, AccountConnectPayload)
    return respond(BooleanResult())


# /api/Account/Delete
@router.post("/api/Account/Delete", name="Account_DeleteAccount")
async def account_delete_account(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(AccountDeletionResult())


# /api/Account/DisconnectAccount/{provider}
@router.post(
    "/api/Account/DisconnectAccount/{provider}", name="Account_DisconnectAccount"
)
async def account_disconnect_account(request: Request, provider: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Account/GetConfirmationCode
@router.post("/api/Account/GetConfirmationCode", name="Account_GetConfirmationCode")
async def account_get_confirmation_code(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(TimedConfirmationCode())


# /api/Account/GetCurrentUserData
@router.get("/api/Account/GetCurrentUserData", name="Account_GetCurrentUserData")
async def account_get_current_user_data(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(UserResult())


# /api/Account/GetPrecedenceTransitionToken
@router.get(
    "/api/Account/GetPrecedenceTransitionToken",
    name="Account_GetPrecedenceTransitionToken",
)
async def account_get_precedence_transition_token(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(TransitionTokenResult())


# /api/Account/GetRoootTransitionToken
@router.get(
    "/api/Account/GetRoootTransitionToken", name="Account_GetRoootTransitionToken"
)
async def account_get_rooot_transition_token(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(TransitionTokenResult())


# /api/Account/GetTakeOverAccount
@router.post("/api/Account/GetTakeOverAccount", name="Account_GetTakeOverAccount")
async def account_get_take_over_account(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, TakeOverAccountPayload)
    return respond(TakeOverAccountResult())


# /api/Account/Register
@router.post("/api/Account/Register", name="Account_Register")
async def account_register(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, RegisterPayload)
    return respond(await register(payload, app))


# /api/Account/RegisterTakeOverPassword
@router.post(
    "/api/Account/RegisterTakeOverPassword", name="Account_RegisterTakeOverPassword"
)
async def account_register_take_over_password(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, RegisterTakeOverPasswordPayload)
    return respond(TakeOverCodeResult())


# /api/Account/TakeOverWithAccountConnect
@router.post(
    "/api/Account/TakeOverWithAccountConnect", name="Account_TakeOverWithAccountConnect"
)
async def account_take_over_with_account_connect(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, AccountConnectPayload)
    return respond(TakeOverAccountResult())


# /api/Account/UpdateBirthDate
@router.post("/api/Account/UpdateBirthDate", name="Account_UpdateBirthDate")
async def account_update_birth_date(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, RegisterBirthDayPayload)
    return respond(BooleanResult())
