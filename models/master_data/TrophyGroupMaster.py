from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from models.enums import TrophyCategories


class TrophyGroupMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    category: TrophyCategories = TrophyCategories.Character
