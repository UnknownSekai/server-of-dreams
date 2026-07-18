from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/Profiles", tags=["Profiles"])


# /api/Profiles/Edit
@router.post("/Edit", response_model=BooleanResult, name="Profile_Edit")
async def profile_edit(body: EditUserProfilePayload) -> BooleanResult:
    return BooleanResult()
