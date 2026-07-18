from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/Gachas", tags=["Gachas"])


# /api/Gachas
@router.get("/", response_model=list[GachaInfoResult], name="Gachas_GetAvailableGachas")
async def gachas_get_available_gachas() -> list[GachaInfoResult]:
    return []
