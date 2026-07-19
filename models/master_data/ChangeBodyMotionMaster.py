from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ChangeBodyMotionMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    before_motion_name: Optional[str] = None
    after_motion_name: Optional[str] = None
    second: float = 0.0
