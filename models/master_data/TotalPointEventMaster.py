from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class TotalPointEventMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    special_event_master_id: int = 0
