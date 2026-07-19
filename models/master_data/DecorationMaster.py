from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import DecorationCategories


class DecorationMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    order: int = 0
    is_default: bool = False
    name: Optional[str] = None
    category: DecorationCategories = DecorationCategories.Special
    widht_px: int = 0
    height_px: int = 0
    min_width_px: int = 0
    max_width_px: int = 0
