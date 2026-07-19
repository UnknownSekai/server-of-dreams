from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import SpineBodySizeTypes


class LoopMotionMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    target_character_base_id: Optional[str] = None
    loop_speed: float = 0.0
    height: int = 0
    size: SpineBodySizeTypes = SpineBodySizeTypes.Small
