from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class CircleEventMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    event_master_id: int = 0
    circle_event_mission_refresh_setting_group_master_id: int = 0
