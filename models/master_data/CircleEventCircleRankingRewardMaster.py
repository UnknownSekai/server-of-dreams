from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class CircleEventCircleRankingRewardMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    circle_event_master_id: int = 0
    circle_event_circle_ranking_reward_item_package_master_id: int = 0
    target_min_rank: int = 0
    target_max_rank: int = 0
