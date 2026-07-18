from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/Possessions", tags=["Possessions"])


# /api/Possessions/SetFavorite
@router.post(
    "/SetFavorite",
    response_model=BooleanResult,
    name="Possessions_BulkSetCostumeFavorite",
)
async def possessions_bulk_set_costume_favorite(
    body: CostumeFavoritePayload,
) -> BooleanResult:
    return BooleanResult()


# /api/Possessions/SortFavoriteStamps
@router.post(
    "/SortFavoriteStamps",
    response_model=BooleanResult,
    name="Possessions_SortFavoriteStamps",
)
async def possessions_sort_favorite_stamps(
    body: FavoriteStampOrderPayload,
) -> BooleanResult:
    return BooleanResult()
