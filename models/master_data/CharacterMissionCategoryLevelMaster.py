from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from models.enums import CharacterMissionCategoryTypes


class CharacterMissionCategoryLevelMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    category_type: CharacterMissionCategoryTypes = CharacterMissionCategoryTypes.Live
    level: int = 0
    give_star_point: int = 0
    start_date: str = ""
    end_date: str = ""
