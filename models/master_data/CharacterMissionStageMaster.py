from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class CharacterMissionStageMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    character_mission_category_level_master_id: int = 0
    character_mission_master_id: int = 0
    exclusion_no_sense_character: bool = False
    order: int = 0
    stage_order: int = 0
    goal_count: int = 0
