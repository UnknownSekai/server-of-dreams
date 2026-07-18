from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import raw_response, read_request, respond
from models import *

router = APIRouter(tags=["Items"])


# /api/Items/ExchangeCharacterPiece
@router.post("/api/Items/ExchangeCharacterPiece", name="Items_ExchangeCharacterPiece")
async def items_exchange_character_piece(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request)
    return respond(ReceivedThing())


# /api/Items/UseBuffItem?itemMasterId=
@router.post("/api/Items/UseBuffItem", name="Items_UseBuffItem")
async def items_use_buff_item(request: Request, itemMasterId: Optional[int] = None):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(BooleanResult())


# /api/Items/UseStaminaRecoveryItems
@router.post("/api/Items/UseStaminaRecoveryItems", name="Items_UseRecoveryStaminaItems")
async def items_use_recovery_stamina_items(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "UseStaminaRecoveryItemsPayload")
    return respond(BooleanResult())
