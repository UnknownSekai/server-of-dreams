from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import ShopReplaceTypes, ShopUnlockTypes, ThingTypes


class ExchangeShopThing(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    thing_id: int = 0
    thing_type: ThingTypes = ThingTypes.Item
    thing_quantity: int = 0
    exchange_limit: Optional[int] = None
    order: int = 0
    replace_type: Optional[ShopReplaceTypes] = None
    is_display_locked: bool = False
    unlock_type: Optional[ShopUnlockTypes] = None
    unlock_value: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    required_item_master_id: int = 0
    required_quantity: int = 0
