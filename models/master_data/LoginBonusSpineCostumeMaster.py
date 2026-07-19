from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class LoginBonusSpineCostumeMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    spine_id: int = 0
    character_base_master_id: int = 0
    target_value: int = 0
    release_date: str = ""
