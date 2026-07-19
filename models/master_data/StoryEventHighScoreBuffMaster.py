from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class StoryEventHighScoreBuffMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    story_event_high_score_buff_pattern_group_id: int = 0
    effect_master_id: int = 0
    effect_name: Optional[str] = None
    effect_description: Optional[str] = None
    icon_image_path: Optional[str] = None
