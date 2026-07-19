from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class PhotoEffectChangeItemMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    item_master_id: int = 0
    photo_effect_type_group_master_id: int = 0
    required_quantity: int = 0
