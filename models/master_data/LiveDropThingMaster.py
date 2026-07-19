from __future__ import annotations

from pydantic import BaseModel

from models.enums import ThingTypes


class LiveDropThingMaster(BaseModel):
    thing_id: int = 0
    thing_type: ThingTypes = ThingTypes.Item
    thing_quantity: int = 0
    is_special_fall_count_up_thing: bool = False
    is_special_fall_thing: bool = False
