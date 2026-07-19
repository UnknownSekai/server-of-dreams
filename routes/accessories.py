from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(tags=["Accessories"])


# /api/Accessories/IncreaseAcquirableAccessoryLimit?toPhase=
@router.post(
    "/api/Accessories/IncreaseAcquirableAccessoryLimit",
    name="Accessories_IncreaseAcquirableAccessoryLimit",
)
async def accessories_increase_acquirable_accessory_limit(
    request: Request, toPhase: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Accessories/{uAccessoryId}/LevelUp/{levelTo}
@router.post(
    "/api/Accessories/{uAccessoryId}/LevelUp/{levelTo}", name="Accessories_LevelUp"
)
async def accessories_level_up(request: Request, uAccessoryId: int, levelTo: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Accessories/Sell
@router.post("/api/Accessories/Sell", name="Accessories_Sell")
async def accessories_sell(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, SellAccessoryPayload)
    return respond(BooleanResult())


# /api/Accessories/SetAccessoryAutoSell?rarityFlag=
@router.post(
    "/api/Accessories/SetAccessoryAutoSell", name="Accessories_SetAccessoryAutoSell"
)
async def accessories_set_accessory_auto_sell(
    request: Request, rarityFlag: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Accessories/SetFavorite
@router.post("/api/Accessories/SetFavorite", name="Accessories_SetAccessoryFavorite")
async def accessories_set_accessory_favorite(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, AccessoryFavoritePayload)
    return respond(BooleanResult())


# /api/Accessories/{accessoryId}/SwitchLock
@router.post("/api/Accessories/{accessoryId}/SwitchLock", name="Accessories_SwitchLock")
async def accessories_switch_lock(request: Request, accessoryId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())
