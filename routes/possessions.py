from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import raw_response, read_request, respond
from models import *

router = APIRouter(tags=["Possessions"])


# /api/Possessions/AddFavoriteStamp/{mStampId}
@router.post(
    "/api/Possessions/AddFavoriteStamp/{mStampId}", name="Possessions_AddFavoriteStamp"
)
async def possessions_add_favorite_stamp(request: Request, mStampId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(BooleanResult())


# /api/Possessions/SetFavorite
@router.post("/api/Possessions/SetFavorite", name="Possessions_BulkSetCostumeFavorite")
async def possessions_bulk_set_costume_favorite(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "CostumeFavoritePayload")
    return respond(BooleanResult())


# /api/Possessions/RemoveFavoriteStamp/{mStampId}
@router.post(
    "/api/Possessions/RemoveFavoriteStamp/{mStampId}",
    name="Possessions_RemoveFavoriteStamp",
)
async def possessions_remove_favorite_stamp(request: Request, mStampId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(BooleanResult())


# /api/Possessions/SortFavoriteStamps
@router.post(
    "/api/Possessions/SortFavoriteStamps", name="Possessions_SortFavoriteStamps"
)
async def possessions_sort_favorite_stamps(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "FavoriteStampOrderPayload")
    return respond(BooleanResult())
