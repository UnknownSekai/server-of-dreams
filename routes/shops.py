from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/Shops", tags=["Shops"])


# /api/Shops/ExchangeMarketThings
@router.post("/ExchangeMarketThings", name="Shops_ExchangeMarketThings")
async def shops_exchange_market_things(request: Request):
    payload = await read_request(request, None)
    return respond([])


# /api/Shops/ExchangeShopThings
@router.post("/ExchangeShopThings", name="Shops_ExchangeShopThings")
async def shops_exchange_shop_things(request: Request):
    payload = await read_request(request, None)
    return respond([])


# /api/Shops/GetOrRefreshMarket
@router.post("/GetOrRefreshMarket", name="Shops_GetOrRefreshMarket")
async def shops_get_or_refresh_market(request: Request):
    return respond(MarketResult())


# /api/Shops/Purchase
@router.post("/Purchase", name="Shops_Purchase")
async def shops_purchase(request: Request):
    payload = await read_request(request, "PurchaseItemPayload")
    return respond([])


# /api/Shops/RefreshMarketWithJewel
@router.post("/RefreshMarketWithJewel", name="Shops_UpdateMarketWithJewel")
async def shops_update_market_with_jewel(request: Request):
    return respond(MarketResult())


# /api/Shops/UpdateLastViewedAt
@router.post("/UpdateLastViewedAt", name="Shops_UpdateLastViewedAt")
async def shops_update_last_viewed_at(request: Request):
    payload = await read_request(request, "UpdateLastViewedAtPayload")
    return respond(BooleanResult())


# /api/Shops/ViewPage
@router.post("/ViewPage", name="Shops_ViewPage")
async def shops_view_page(request: Request):
    return respond(ViewShopResult())
