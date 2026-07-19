from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PhotoEffectMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name: Optional[str] = None
    description: Optional[str] = None
    effect_master_id: int = 0
    variety: Optional[int] = None
    photo_effect_type_group_master_id: Optional[int] = None
    photo_effect_group_master_id: int = 0
