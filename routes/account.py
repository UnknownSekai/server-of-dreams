from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/Account", tags=["Account"])


# /api/Account/Authenticate
@router.post(
    "/Authenticate", response_model=AuthenticateResult, name="Account_Authenticate"
)
async def account_authenticate(body: AuthenticatePayload) -> AuthenticateResult:
    return AuthenticateResult()


# /api/Account/ConnectAccount
@router.post(
    "/ConnectAccount", response_model=BooleanResult, name="Account_ConnectAccount"
)
async def account_connect_account(body: AccountConnectPayload) -> BooleanResult:
    return BooleanResult()


# /api/Account/Delete
@router.post(
    "/Delete", response_model=AccountDeletionResult, name="Account_DeleteAccount"
)
async def account_delete_account() -> AccountDeletionResult:
    return AccountDeletionResult()


# /api/Account/GetConfirmationCode
@router.post(
    "/GetConfirmationCode",
    response_model=TimedConfirmationCode,
    name="Account_GetConfirmationCode",
)
async def account_get_confirmation_code() -> TimedConfirmationCode:
    return TimedConfirmationCode()


# /api/Account/GetCurrentUserData
@router.get(
    "/GetCurrentUserData", response_model=UserResult, name="Account_GetCurrentUserData"
)
async def account_get_current_user_data() -> UserResult:
    return UserResult()


# /api/Account/GetPrecedenceTransitionToken
@router.get(
    "/GetPrecedenceTransitionToken",
    response_model=TransitionTokenResult,
    name="Account_GetPrecedenceTransitionToken",
)
async def account_get_precedence_transition_token() -> TransitionTokenResult:
    return TransitionTokenResult()


# /api/Account/GetRoootTransitionToken
@router.get(
    "/GetRoootTransitionToken",
    response_model=TransitionTokenResult,
    name="Account_GetRoootTransitionToken",
)
async def account_get_rooot_transition_token() -> TransitionTokenResult:
    return TransitionTokenResult()


# /api/Account/GetTakeOverAccount
@router.post(
    "/GetTakeOverAccount",
    response_model=TakeOverAccountResult,
    name="Account_GetTakeOverAccount",
)
async def account_get_take_over_account(
    body: TakeOverAccountPayload,
) -> TakeOverAccountResult:
    return TakeOverAccountResult()


# /api/Account/Register
@router.post("/Register", response_model=AccountRegistResult, name="Account_Register")
async def account_register(body: RegisterPayload) -> AccountRegistResult:
    return AccountRegistResult()


# /api/Account/RegisterTakeOverPassword
@router.post(
    "/RegisterTakeOverPassword",
    response_model=TakeOverCodeResult,
    name="Account_RegisterTakeOverPassword",
)
async def account_register_take_over_password(
    body: RegisterTakeOverPasswordPayload,
) -> TakeOverCodeResult:
    return TakeOverCodeResult()


# /api/Account/TakeOverWithAccountConnect
@router.post(
    "/TakeOverWithAccountConnect",
    response_model=TakeOverAccountResult,
    name="Account_TakeOverWithAccountConnect",
)
async def account_take_over_with_account_connect(
    body: AccountConnectPayload,
) -> TakeOverAccountResult:
    return TakeOverAccountResult()


# /api/Account/UpdateBirthDate
@router.post(
    "/UpdateBirthDate", response_model=BooleanResult, name="Account_UpdateBirthDate"
)
async def account_update_birth_date(body: RegisterBirthDayPayload) -> BooleanResult:
    return BooleanResult()
