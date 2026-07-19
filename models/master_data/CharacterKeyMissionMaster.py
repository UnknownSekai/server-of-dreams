from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CharacterKeyMissionMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    level: int = 0
    color: Optional[str] = None
    give_star_point: int = 0
    start_date: str = ""
    end_date: str = ""
    required_category_count: int = 0
