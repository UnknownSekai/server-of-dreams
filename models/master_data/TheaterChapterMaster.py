from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .TheaterStoryMaster import TheaterStoryMaster


class TheaterChapterMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name: Optional[str] = None
    company_master_id: int = 0
    display_start_at: str = ""
    display_end_at: str = ""
    stories: Optional[list[TheaterStoryMaster]] = None
    episode_master_id: Optional[int] = None
    required_read_episode_master_id: int = 0
    theater_story_master_ids: Optional[list[int]] = None
