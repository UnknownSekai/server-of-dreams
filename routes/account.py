from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from helpers.auth import authenticate, register
from models import *

router = APIRouter(prefix="/api/Account", tags=["Account"])


# /api/Account/Authenticate
@router.post("/Authenticate", name="Account_Authenticate")
async def account_authenticate(request: Request):
    payload = await read_request(request, "AuthenticatePayload")
    return respond(authenticate(payload))


# /api/Account/ConnectAccount
@router.post("/ConnectAccount", name="Account_ConnectAccount")
async def account_connect_account(request: Request):
    payload = await read_request(request, "AccountConnectPayload")
    return respond(BooleanResult())


# /api/Account/Delete
@router.post("/Delete", name="Account_DeleteAccount")
async def account_delete_account(request: Request):
    return respond(AccountDeletionResult())


# /api/Account/GetConfirmationCode
@router.post("/GetConfirmationCode", name="Account_GetConfirmationCode")
async def account_get_confirmation_code(request: Request):
    return respond(TimedConfirmationCode())


# /api/Account/GetCurrentUserData
@router.get("/GetCurrentUserData", name="Account_GetCurrentUserData")
async def account_get_current_user_data(request: Request):
    return respond(UserResult())


# /api/Account/GetPrecedenceTransitionToken
@router.get(
    "/GetPrecedenceTransitionToken", name="Account_GetPrecedenceTransitionToken"
)
async def account_get_precedence_transition_token(request: Request):
    return respond(TransitionTokenResult())


# /api/Account/GetRoootTransitionToken
@router.get("/GetRoootTransitionToken", name="Account_GetRoootTransitionToken")
async def account_get_rooot_transition_token(request: Request):
    return respond(TransitionTokenResult())


# /api/Account/GetTakeOverAccount
@router.post("/GetTakeOverAccount", name="Account_GetTakeOverAccount")
async def account_get_take_over_account(request: Request):
    payload = await read_request(request, "TakeOverAccountPayload")
    return respond(TakeOverAccountResult())


# /api/Account/Register
@router.post("/Register", name="Account_Register")
async def account_register(request: Request):
    payload = await read_request(request, "RegisterPayload")
    return respond(register(payload))


# /api/Account/RegisterTakeOverPassword
@router.post("/RegisterTakeOverPassword", name="Account_RegisterTakeOverPassword")
async def account_register_take_over_password(request: Request):
    payload = await read_request(request, "RegisterTakeOverPasswordPayload")
    return respond(TakeOverCodeResult())


# /api/Account/TakeOverWithAccountConnect
@router.post("/TakeOverWithAccountConnect", name="Account_TakeOverWithAccountConnect")
async def account_take_over_with_account_connect(request: Request):
    payload = await read_request(request, "AccountConnectPayload")
    return respond(TakeOverAccountResult())


# /api/Account/UpdateBirthDate
@router.post("/UpdateBirthDate", name="Account_UpdateBirthDate")
async def account_update_birth_date(request: Request):
    payload = await read_request(request, "RegisterBirthDayPayload")
    return respond(BooleanResult())
