from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/Accessories", tags=["Accessories"])


# /api/Accessories/Sell
@router.post("/Sell", response_model=BooleanResult, name="Accessories_Sell")
async def accessories_sell(body: SellAccessoryPayload) -> BooleanResult:
    return BooleanResult()


# /api/Accessories/SetFavorite
@router.post(
    "/SetFavorite",
    response_model=BooleanResult,
    name="Accessories_SetAccessoryFavorite",
)
async def accessories_set_accessory_favorite(
    body: AccessoryFavoritePayload,
) -> BooleanResult:
    return BooleanResult()
