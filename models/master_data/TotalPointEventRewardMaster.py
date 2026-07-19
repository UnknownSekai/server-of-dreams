from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from models.enums import ThingTypes


class TotalPointEventRewardMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    total_point_event_master_id: int = 0
    point: int = 0
    thing_type: ThingTypes = ThingTypes.Item
    thing_id: int = 0
    thing_quantity: int = 0
    order: int = 0
