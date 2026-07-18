from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/Possessions", tags=["Possessions"])


# /api/Possessions/SetFavorite
@router.post("/SetFavorite", name="Possessions_BulkSetCostumeFavorite")
async def possessions_bulk_set_costume_favorite(request: Request):
    payload = await read_request(request, "CostumeFavoritePayload")
    return respond(BooleanResult())


# /api/Possessions/SortFavoriteStamps
@router.post("/SortFavoriteStamps", name="Possessions_SortFavoriteStamps")
async def possessions_sort_favorite_stamps(request: Request):
    payload = await read_request(request, "FavoriteStampOrderPayload")
    return respond(BooleanResult())
