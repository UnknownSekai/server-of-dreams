from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from models.enums import EventStoryListFlags


class StoryEventStoryMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    story_master_id: int = 0
    story_event_master_id: int = 0
    listed_start_date: str = ""
    event_story_list_flags: EventStoryListFlags = EventStoryListFlags.Sirius
    is_key_story: bool = False
