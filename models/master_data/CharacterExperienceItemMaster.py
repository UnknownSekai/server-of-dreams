from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class CharacterExperienceItemMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    item_master_id: int = 0
    acquirable_experience: int = 0
    acquirable_experience_bonus: float = 0.0
