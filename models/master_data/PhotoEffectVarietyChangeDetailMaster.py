from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class PhotoEffectVarietyChangeDetailMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    before_photo_effect_max_variety: int = 0
    after_photo_effect_max_variety: int = 0
    before_variety: int = 0
    after_variety: int = 0
