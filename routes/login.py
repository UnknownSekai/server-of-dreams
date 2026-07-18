from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/Login", tags=["Login"])


# /api/Login
@router.post("/", response_model=LoginResult, name="Login_Login")
async def login_login(body: LoginPayload) -> LoginResult:
    return LoginResult()
