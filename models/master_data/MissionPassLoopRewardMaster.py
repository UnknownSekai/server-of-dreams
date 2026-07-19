from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .MissionPassLoopRewardThingMaster import MissionPassLoopRewardThingMaster


class MissionPassLoopRewardMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    phase: int = 0
    start_date: str = ""
    end_date: str = ""
    rewards: Optional[list[MissionPassLoopRewardThingMaster]] = None
