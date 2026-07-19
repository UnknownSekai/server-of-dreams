from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .EpisodeReleaseCondition import EpisodeReleaseCondition


class EpisodeMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    story_master_id: int = 0
    title: Optional[str] = None
    order: int = 0
    episode_reward_package_master_id: int = 0
    conditions: Optional[list[EpisodeReleaseCondition]] = None
    pre_episode_master_id: Optional[int] = None
    display_start_date: Optional[str] = None
    display_end_date: Optional[str] = None
