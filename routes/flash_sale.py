from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/FlashSale", tags=["FlashSale"])


# /api/FlashSale/ReadFlashSaleStage
@router.post(
    "/ReadFlashSaleStage",
    response_model=BooleanResult,
    name="FlashSale_ReadFlashSaleStage",
)
async def flash_sale_read_flash_sale_stage(
    body: FlashSaleReadStagePayload,
) -> BooleanResult:
    return BooleanResult()
