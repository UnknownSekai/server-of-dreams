from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import PosterEpisodeTypes


class PosterStoryMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    poster_master_id: int = 0
    episode_type: PosterEpisodeTypes = PosterEpisodeTypes.Information
    character_base_master_id: Optional[int] = None
    description: Optional[str] = None
    order: int = 0
    character_icon_id: Optional[int] = None
    character_name: Optional[str] = None
