from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class MusicVideoDefaultCostumeMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    character_base_master_id: int = 0
    costume_master_id: int = 0
