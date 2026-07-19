from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CircleTheaterLevelMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    level: int = 0
    stamina_base_value: int = 0
    description: Optional[str] = None
