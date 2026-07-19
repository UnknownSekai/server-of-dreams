from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class PickupCharacterMissionMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    character_master_id: int = 0
    order: int = 0
    pickup_character_mission_detail_group_master_id: int = 0
    start_date: str = ""
    end_date: str = ""
