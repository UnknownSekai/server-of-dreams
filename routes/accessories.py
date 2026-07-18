from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/Accessories", tags=["Accessories"])


# /api/Accessories/Sell
@router.post("/Sell", name="Accessories_Sell")
async def accessories_sell(request: Request):
    payload = await read_request(request, "SellAccessoryPayload")
    return respond(BooleanResult())


# /api/Accessories/SetFavorite
@router.post("/SetFavorite", name="Accessories_SetAccessoryFavorite")
async def accessories_set_accessory_favorite(request: Request):
    payload = await read_request(request, "AccessoryFavoritePayload")
    return respond(BooleanResult())
