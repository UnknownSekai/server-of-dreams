from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(tags=["FlashSale"])


# /api/FlashSale/ReadFlashSaleStage
@router.post("/api/FlashSale/ReadFlashSaleStage", name="FlashSale_ReadFlashSaleStage")
async def flash_sale_read_flash_sale_stage(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, FlashSaleReadStagePayload)
    return respond(BooleanResult())
