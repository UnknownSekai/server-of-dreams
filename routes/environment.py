from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/Environment", tags=["Environment"])


# /api/Environment/Ping
@router.get("/Ping", response_model=BooleanResult, name="Environment_Ping")
async def environment_ping() -> BooleanResult:
    return BooleanResult()
