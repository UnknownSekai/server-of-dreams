from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CategoryGroupMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    order: int = 0
    name: Optional[str] = None
    color_code: Optional[str] = None
