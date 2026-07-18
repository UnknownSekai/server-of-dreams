from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/Photo", tags=["Photo"])


# /api/Photo/AbilityVarietyUp
@router.post(
    "/AbilityVarietyUp", response_model=BooleanResult, name="Photo_AbilityVarietyUp"
)
async def photo_ability_variety_up(body: AbilityVarietyUpPayload) -> BooleanResult:
    return BooleanResult()


# /api/Photo/AlbumDetailArranging
@router.post(
    "/AlbumDetailArranging",
    response_model=BooleanResult,
    name="Photo_AlbumDetailArranging",
)
async def photo_album_detail_arranging(body: AlbumArrangingPayload) -> BooleanResult:
    return BooleanResult()


# /api/Photo/AlbumSimpleArranging
@router.post(
    "/AlbumSimpleArranging",
    response_model=BooleanResult,
    name="Photo_AlbumSimpleArranging",
)
async def photo_album_simple_arranging(body: AlbumArrangingPayload) -> BooleanResult:
    return BooleanResult()


# /api/Photo/ChangePhotoAbility
@router.post(
    "/ChangePhotoAbility", response_model=BooleanResult, name="Photo_ChangePhotoAbility"
)
async def photo_change_photo_ability(body: ChangePhotoAbilityPayload) -> BooleanResult:
    return BooleanResult()


# /api/Photo/GetAlbumMainPage?targetUserId=
@router.post(
    "/GetAlbumMainPage",
    response_model=AlbumPageSearchResult,
    name="Photo_GetAlbumMainPage",
)
async def photo_get_album_main_page(targetUserId: str) -> AlbumPageSearchResult:
    return AlbumPageSearchResult()


# /api/Photo/SetAlbumPublishing
@router.post(
    "/SetAlbumPublishing", response_model=BooleanResult, name="Photo_SetAlbumPublishing"
)
async def photo_set_album_publishing(body: SetAlbumPublishingPayload) -> BooleanResult:
    return BooleanResult()


# /api/Photo/SetCharacterBaseTags
@router.post(
    "/SetCharacterBaseTags",
    response_model=BooleanResult,
    name="Photo_SetCharacterBaseTags",
)
async def photo_set_character_base_tags(body: SetPhotoTagPayload) -> BooleanResult:
    return BooleanResult()
