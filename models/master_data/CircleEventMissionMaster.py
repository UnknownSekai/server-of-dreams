from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import CircleEventMissionTypes, JumpTypes


class CircleEventMissionMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    circle_event_master_id: int = 0
    mission_category: CircleEventMissionTypes = CircleEventMissionTypes.Individual
    title: Optional[str] = None
    jump_type: JumpTypes = JumpTypes.None_
    jump_target_id: Optional[int] = None
    goal_count: int = 0
    give_point_at_goal: int = 0
    circle_goal_count: int = 0
    circle_give_point_at_goal: int = 0
    is_default: bool = False
