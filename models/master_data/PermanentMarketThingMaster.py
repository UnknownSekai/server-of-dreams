from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import ShopUnlockTypes, ThingTypes


class PermanentMarketThingMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    thing_id: int = 0
    thing_type: ThingTypes = ThingTypes.Item
    thing_quantity: int = 0
    exchange_limit: Optional[int] = None
    order: int = 0
    unlock_type: Optional[ShopUnlockTypes] = None
    unlock_value: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    required_thing_type: ThingTypes = ThingTypes.Item
    required_thing_id: int = 0
    required_thing_quantity: int = 0
