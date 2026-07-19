from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class StoryEventStoryBgmSchedule(BaseModel):
    asset_name: Optional[str] = None
    start_date: str = ""
    end_date: str = ""
