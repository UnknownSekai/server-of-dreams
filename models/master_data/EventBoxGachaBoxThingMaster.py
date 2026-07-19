from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from models.enums import ThingTypes


class EventBoxGachaBoxThingMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    thing_id: int = 0
    thing_type: ThingTypes = ThingTypes.Item
    thing_quantity: int = 0
    hit_limit: int = 0
    is_resettable: bool = False
