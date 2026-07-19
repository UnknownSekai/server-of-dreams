from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class StarActConditionMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    free_light: int = 0
    support_light: int = 0
    control_light: int = 0
    amplification_light: int = 0
    special_light: int = 0
