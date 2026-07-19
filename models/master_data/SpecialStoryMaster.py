from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import EventStoryListFlags


class SpecialStoryMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    story_master_id: int = 0
    start_date: str = ""
    end_date: str = ""
    event_story_list_flags: EventStoryListFlags = EventStoryListFlags.Sirius
    title: Optional[str] = None
    order: int = 0
