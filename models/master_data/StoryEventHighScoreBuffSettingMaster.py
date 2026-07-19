from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .StoryEventHighScoreBuffMaster import StoryEventHighScoreBuffMaster


class StoryEventHighScoreBuffSettingMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    story_event_high_score_master_id: int = 0
    story_event_high_score_buff_master_id: int = 0
    story_event_high_score_buff_master: Optional[StoryEventHighScoreBuffMaster] = None
