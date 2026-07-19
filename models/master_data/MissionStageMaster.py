from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .MissionRewardMaster import MissionRewardMaster


class MissionStageMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    mission_stage_order: int = 0
    stage_goal_value: int = 0
    start_date: Optional[str] = None
    rewards: Optional[list[MissionRewardMaster]] = None
