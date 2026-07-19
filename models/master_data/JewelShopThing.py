from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from models.enums import ThingTypes


class JewelShopThing(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    m_jewel_shop_item_id: int = 0
    thing_id: int = 0
    thing_type: ThingTypes = ThingTypes.Item
    thing_quantity: int = 0
