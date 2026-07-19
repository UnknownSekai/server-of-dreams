from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CategoryMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    category_group_master_id: int = 0
    order: int = 0
    name: Optional[str] = None
