from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class HeadMotionMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    motion_name: Optional[str] = None
