from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class StoryEventRewardMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    story_event_master_id: int = 0
    target_min_rank: int = 0
    target_max_rank: int = 0
    story_event_reward_item_package_id: int = 0
