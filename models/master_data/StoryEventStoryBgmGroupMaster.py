from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from .StoryEventStoryBgmSchedule import StoryEventStoryBgmSchedule


class StoryEventStoryBgmGroupMaster(BaseModel):
    story_event_master_id: int = 0
    schedules: Optional[list[StoryEventStoryBgmSchedule]] = None
