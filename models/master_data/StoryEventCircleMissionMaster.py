from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class StoryEventCircleMissionMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    story_event_master_id: int = 0
    title: Optional[str] = None
    count_unit: Optional[str] = None
    goal_count: int = 0
    max_phase: int = 0
    give_point_at_goal: int = 0
