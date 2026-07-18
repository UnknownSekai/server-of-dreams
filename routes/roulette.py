from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import raw_response, read_request, respond
from models import *

router = APIRouter(tags=["Roulette"])


# /api/Roulettes/Roll?mRouletteId=&rollCount=
@router.post("/api/Roulettes/Roll", name="Roulette_Roll")
async def roulette_roll(
    request: Request, mRouletteId: Optional[int] = None, rollCount: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(RouletteRollResult())
