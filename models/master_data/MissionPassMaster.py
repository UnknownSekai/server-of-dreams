from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class MissionPassMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    item_master_id: int = 0
    start_date: str = ""
    end_date: str = ""
