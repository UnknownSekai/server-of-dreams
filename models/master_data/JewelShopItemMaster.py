from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import (
    JewelShopUnlockTypes,
    SaleTypes,
    ShopItemTypes,
    ShopPurchaseTypes,
    ShopReplaceTypes,
)

if TYPE_CHECKING:
    from .JewelShopThing import JewelShopThing


class JewelShopItemMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    order: int = 0
    app_store_product_id: Optional[str] = None
    google_play_product_id: Optional[str] = None
    name: Optional[str] = None
    pack_text: Optional[str] = None
    m_jewel_shop_category_id: int = 0
    dialog_type: int = 0
    purchase_type: ShopPurchaseTypes = ShopPurchaseTypes.Paid
    purchase_value: Optional[int] = None
    subscription_flag: bool = False
    give_paid_jewel: Optional[int] = None
    replace_types: Optional[ShopReplaceTypes] = None
    replace_value: Optional[int] = None
    purchase_limit: Optional[int] = None
    expired_day: Optional[int] = None
    can_purchase_day_of_week: Optional[str] = None
    is_buy_not_display: bool = False
    sale_type: Optional[SaleTypes] = None
    sale_value: Optional[int] = None
    is_display_locking: bool = False
    unlock_type: Optional[JewelShopUnlockTypes] = None
    unlock_value: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    lineup: Optional[list[JewelShopThing]] = None
    shop_item_type: ShopItemTypes = ShopItemTypes.None_
    shop_item_value: Optional[int] = None
    comeback_campaign_master_id: Optional[int] = None
    item_icon_body_image_path: Optional[str] = None
    item_icon_detail_image_path: Optional[str] = None
    item_icon_badge_image_path: Optional[str] = None
