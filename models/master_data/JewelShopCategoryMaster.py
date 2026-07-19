from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class JewelShopCategoryMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name: Optional[str] = None
    layout_type: int = 0
    is_display_locking: Optional[int] = None
    banner_path: Optional[str] = None
    order: int = 0
