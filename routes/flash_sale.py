from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/FlashSale", tags=["FlashSale"])


# /api/FlashSale/ReadFlashSaleStage
@router.post("/ReadFlashSaleStage", name="FlashSale_ReadFlashSaleStage")
async def flash_sale_read_flash_sale_stage(request: Request):
    payload = await read_request(request, "FlashSaleReadStagePayload")
    return respond(BooleanResult())
