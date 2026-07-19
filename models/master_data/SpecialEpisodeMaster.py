from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SpecialEpisodeMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    story_master_id: int = 0
    title: Optional[str] = None
    required_read_episode_master_id: Optional[int] = None
