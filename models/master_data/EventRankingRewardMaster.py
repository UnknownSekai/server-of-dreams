from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .EventRankingRewardThingMaster import EventRankingRewardThingMaster


class EventRankingRewardMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    target_highest_rank: int = 0
    target_lowest_rank: int = 0
    rewards: Optional[list[EventRankingRewardThingMaster]] = None
