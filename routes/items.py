from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/Items", tags=["Items"])


# /api/Items/ExchangeCharacterPiece
@router.post("/ExchangeCharacterPiece", name="Items_ExchangeCharacterPiece")
async def items_exchange_character_piece(request: Request):
    payload = await read_request(request, None)
    return respond(ReceivedThing())


# /api/Items/UseStaminaRecoveryItems
@router.post("/UseStaminaRecoveryItems", name="Items_UseRecoveryStaminaItems")
async def items_use_recovery_stamina_items(request: Request):
    payload = await read_request(request, "UseStaminaRecoveryItemsPayload")
    return respond(BooleanResult())
