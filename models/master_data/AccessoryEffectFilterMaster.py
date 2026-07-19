from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import EffectTypes


class AccessoryEffectFilterMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    effect_type: EffectTypes = EffectTypes.BaseVocalUp
    name: Optional[str] = None
    start_date: str = ""
    order: int = 0
