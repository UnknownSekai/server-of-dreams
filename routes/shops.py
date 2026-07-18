from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import raw_response, read_request, respond
from models import *

router = APIRouter(tags=["Shops"])


# /api/Shops/ExchangeMarketThing/{number}
@router.post(
    "/api/Shops/ExchangeMarketThing/{number}", name="Shops_ExchangeMarketThing"
)
async def shops_exchange_market_thing(request: Request, number: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response([])


# /api/Shops/ExchangeMarketThings
@router.post("/api/Shops/ExchangeMarketThings", name="Shops_ExchangeMarketThings")
async def shops_exchange_market_things(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request)
    return respond([])


# /api/Shops/ExchangeMusic/{mMusicId}
@router.post("/api/Shops/ExchangeMusic/{mMusicId}", name="Shops_ExchangeMusic")
async def shops_exchange_music(request: Request, mMusicId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(ReceivedThing())


# /api/Shops/ExchangeMusicScore/{mLiveId}
@router.post("/api/Shops/ExchangeMusicScore/{mLiveId}", name="Shops_ExchangeMusicScore")
async def shops_exchange_music_score(request: Request, mLiveId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(BooleanResult())


# /api/Shops/ExchangePermanentMarketThing/{PermanentMarketThingMasterid}?permanentMarketThingMasterId=&quantity=
@router.post(
    "/api/Shops/ExchangePermanentMarketThing/{PermanentMarketThingMasterid}",
    name="Shops_ExchangePermanentMarketThings",
)
async def shops_exchange_permanent_market_things(
    request: Request,
    PermanentMarketThingMasterid: int,
    permanentMarketThingMasterId: Optional[int] = None,
    quantity: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response([])


# /api/Shops/ExchangeShopThing/{mExchangeShopThingId}/{quantity}
@router.post(
    "/api/Shops/ExchangeShopThing/{mExchangeShopThingId}/{quantity}",
    name="Shops_ExchangeShopThing",
)
async def shops_exchange_shop_thing(
    request: Request, mExchangeShopThingId: int, quantity: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response([])


# /api/Shops/ExchangeShopThings
@router.post("/api/Shops/ExchangeShopThings", name="Shops_ExchangeShopThings")
async def shops_exchange_shop_things(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "ExchangeShopThingPayload")
    return respond([])


# /api/Shops/GetOrRefreshMarket
@router.post("/api/Shops/GetOrRefreshMarket", name="Shops_GetOrRefreshMarket")
async def shops_get_or_refresh_market(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(MarketResult())


# /api/Shops/Purchase
@router.post("/api/Shops/Purchase", name="Shops_Purchase")
async def shops_purchase(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "PurchaseItemPayload")
    return respond([])


# /api/Shops/UpdateLastViewedAt
@router.post("/api/Shops/UpdateLastViewedAt", name="Shops_UpdateLastViewedAt")
async def shops_update_last_viewed_at(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "UpdateLastViewedAtPayload")
    return respond(BooleanResult())


# /api/Shops/RefreshMarketWithJewel
@router.post("/api/Shops/RefreshMarketWithJewel", name="Shops_UpdateMarketWithJewel")
async def shops_update_market_with_jewel(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(MarketResult())


# /api/Shops/ViewPage
@router.post("/api/Shops/ViewPage", name="Shops_ViewPage")
async def shops_view_page(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(ViewShopResult())
