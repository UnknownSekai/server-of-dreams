from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from models.enums import MarketDisplayTypes, ThingTypes


class MarketFrameThingMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    thing_id: int = 0
    thing_type: ThingTypes = ThingTypes.Item
    thing_quantity: int = 0
    required_thing_type: ThingTypes = ThingTypes.Item
    required_thing_id: int = 0
    required_thing_quantity: int = 0
    display_type: MarketDisplayTypes = MarketDisplayTypes.Default
