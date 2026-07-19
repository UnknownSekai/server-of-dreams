from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class MusicGroupDetailMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    music_group_master_id: int = 0
    music_master_id: int = 0
