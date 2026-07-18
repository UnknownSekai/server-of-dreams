from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/Items", tags=["Items"])


# /api/Items/ExchangeCharacterPiece
@router.post(
    "/ExchangeCharacterPiece",
    response_model=ReceivedThing,
    name="Items_ExchangeCharacterPiece",
)
async def items_exchange_character_piece(body: list[int]) -> ReceivedThing:
    return ReceivedThing()


# /api/Items/UseStaminaRecoveryItems
@router.post(
    "/UseStaminaRecoveryItems",
    response_model=BooleanResult,
    name="Items_UseRecoveryStaminaItems",
)
async def items_use_recovery_stamina_items(
    body: UseStaminaRecoveryItemsPayload,
) -> BooleanResult:
    return BooleanResult()
