from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AccessoryEffectMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    effect_master_id: int = 0
    name: Optional[str] = None
    description: Optional[str] = None
    variety: Optional[int] = None
