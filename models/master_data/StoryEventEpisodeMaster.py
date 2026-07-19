from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class StoryEventEpisodeMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    story_master_id: int = 0
    required_total_acquired_point: int = 0
    title: Optional[str] = None
    order: int = 0
    required_read_episode_master_id: Optional[int] = None
    episode_reward_package_master_id: int = 0
