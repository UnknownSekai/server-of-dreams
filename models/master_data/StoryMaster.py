from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import StoryTypes


class StoryMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    type: StoryTypes = StoryTypes.None_
    company_master_id: Optional[int] = None
    event_master_id: Optional[int] = None
    chapter_order: int = 0
    display_start_at: str = ""
    display_end_at: str = ""
