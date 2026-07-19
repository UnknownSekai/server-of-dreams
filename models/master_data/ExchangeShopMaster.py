from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import ShopCategories, ThingTypes

if TYPE_CHECKING:
    from .ExchangeShopThing import ExchangeShopThing


class ExchangeShopMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    is_display_required_having_item: bool = False
    category: ShopCategories = ShopCategories.None_
    name: Optional[str] = None
    display_thing_type: ThingTypes = ThingTypes.Item
    display_item_master_id: Optional[int] = None
    banner_path: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    last_refreshed_at: str = ""
    lineup: Optional[list[ExchangeShopThing]] = None
    order: int = 0
