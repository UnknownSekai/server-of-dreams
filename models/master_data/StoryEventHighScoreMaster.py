from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class StoryEventHighScoreMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    story_event_master_id: int = 0
    music_master_id: int = 0
    buff_ids: Optional[list[int]] = None
    sense_notation_master_id: int = 0
