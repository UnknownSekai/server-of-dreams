from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/Characters", tags=["Characters"])


# /api/Characters/BulkLevelUp
@router.post(
    "/BulkLevelUp", response_model=BooleanResult, name="Characters_BulkLevelUp"
)
async def characters_bulk_level_up(body: list[BulkLevelUpPayload]) -> BooleanResult:
    return BooleanResult()


# /api/Characters/Portal/SetCharacter
@router.post(
    "/Portal/SetCharacter",
    response_model=BooleanResult,
    name="Characters_SetPortalMCharacter",
)
async def characters_set_portal_m_character(
    body: ActorPortalCharacterPayload,
) -> BooleanResult:
    return BooleanResult()


# /api/Characters/SetFavorite
@router.post(
    "/SetFavorite", response_model=BooleanResult, name="Characters_SetCharacterFavorite"
)
async def characters_set_character_favorite(
    body: CharacterFavoritePayload,
) -> BooleanResult:
    return BooleanResult()
