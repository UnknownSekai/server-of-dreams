from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class PickupSelectionGachaMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    gacha_master_id: int = 0
    min_select_count: int = 0
    max_select_count: int = 0
    fixed_prize_pickup_only: bool = False
