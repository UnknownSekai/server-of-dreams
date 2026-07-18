from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/Photos", tags=["Photos"])


# /api/Photos/FinishGeneratePhoto
@router.post(
    "/FinishGeneratePhoto",
    response_model=BooleanResult,
    name="Photo_FinishGeneratePhoto",
)
async def photo_finish_generate_photo() -> BooleanResult:
    return BooleanResult()


# /api/Photos/GeneratePhoto
@router.post(
    "/GeneratePhoto", response_model=GeneratePhotoResult, name="Photo_GeneratePhoto"
)
async def photo_generate_photo(body: GeneratePhotoPayload) -> GeneratePhotoResult:
    return GeneratePhotoResult()


# /api/Photos/GeneratePhotos
@router.post(
    "/GeneratePhotos",
    response_model=list[GeneratePhotoResult],
    name="Photo_GeneratePhotos",
)
async def photo_generate_photos(
    body: GeneratePhotosPayload,
) -> list[GeneratePhotoResult]:
    return []


# /api/Photos/PhotoLevelUp
@router.post(
    "/PhotoLevelUp", response_model=LevelUpPhotoResult, name="Photo_PhotoLevelUp"
)
async def photo_photo_level_up(body: LevelUpPhotoPayload) -> LevelUpPhotoResult:
    return LevelUpPhotoResult()


# /api/Photos/Sell
@router.post("/Sell", response_model=BooleanResult, name="Photo_Sell")
async def photo_sell(body: list[int]) -> BooleanResult:
    return BooleanResult()
