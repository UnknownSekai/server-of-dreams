from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/Posters", tags=["Posters"])


# /api/Posters/ChangePosterAlternativeImage
@router.post(
    "/ChangePosterAlternativeImage",
    response_model=BooleanResult,
    name="Posters_ChangePosterAlternativeImage",
)
async def posters_change_poster_alternative_image(
    body: PosterAlternativeImagePayload,
) -> BooleanResult:
    return BooleanResult()


# /api/Posters/SetFavorite
@router.post(
    "/SetFavorite", response_model=BooleanResult, name="Posters_SetPosterFavorite"
)
async def posters_set_poster_favorite(body: PosterFavoritePayload) -> BooleanResult:
    return BooleanResult()
