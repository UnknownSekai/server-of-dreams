from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class PosterLevelPatternMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    level_pattern_group_id: int = 0
    level: int = 0
    item_master_id: int = 0
    quantity: int = 0
