from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class LightLoadSplitEffectMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    base_effect: int = 0
    light_load_effect: int = 0
