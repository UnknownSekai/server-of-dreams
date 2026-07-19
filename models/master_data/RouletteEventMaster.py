from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class RouletteEventMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    event_master_id: int = 0
    roulette_point_item_master_id: int = 0
