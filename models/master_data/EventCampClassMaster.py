from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class EventCampClassMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    event_master_id: int = 0
    target_max_rank: int = 0
    target_min_rank: int = 0
    reward_receive_ratio: int = 0
