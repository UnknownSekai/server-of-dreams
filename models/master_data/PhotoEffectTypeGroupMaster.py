from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PhotoEffectTypeGroupMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    photo_effect_max_variety: int = 0
    description: Optional[str] = None
    can_use_item: bool = False
