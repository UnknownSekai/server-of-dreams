from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/Shops", tags=["Shops"])


# /api/Shops/ExchangeMarketThings
@router.post(
    "/ExchangeMarketThings",
    response_model=list[ReceivedThing],
    name="Shops_ExchangeMarketThings",
)
async def shops_exchange_market_things(body: list[int]) -> list[ReceivedThing]:
    return []


# /api/Shops/ExchangeShopThings
@router.post(
    "/ExchangeShopThings",
    response_model=list[ReceivedThing],
    name="Shops_ExchangeShopThings",
)
async def shops_exchange_shop_things(
    body: list[ExchangeShopThingPayload],
) -> list[ReceivedThing]:
    return []


# /api/Shops/GetOrRefreshMarket
@router.post(
    "/GetOrRefreshMarket", response_model=MarketResult, name="Shops_GetOrRefreshMarket"
)
async def shops_get_or_refresh_market() -> MarketResult:
    return MarketResult()


# /api/Shops/Purchase
@router.post("/Purchase", response_model=list[ReceivedThing], name="Shops_Purchase")
async def shops_purchase(body: PurchaseItemPayload) -> list[ReceivedThing]:
    return []


# /api/Shops/RefreshMarketWithJewel
@router.post(
    "/RefreshMarketWithJewel",
    response_model=MarketResult,
    name="Shops_UpdateMarketWithJewel",
)
async def shops_update_market_with_jewel() -> MarketResult:
    return MarketResult()


# /api/Shops/UpdateLastViewedAt
@router.post(
    "/UpdateLastViewedAt", response_model=BooleanResult, name="Shops_UpdateLastViewedAt"
)
async def shops_update_last_viewed_at(body: UpdateLastViewedAtPayload) -> BooleanResult:
    return BooleanResult()


# /api/Shops/ViewPage
@router.post("/ViewPage", response_model=ViewShopResult, name="Shops_ViewPage")
async def shops_view_page() -> ViewShopResult:
    return ViewShopResult()
