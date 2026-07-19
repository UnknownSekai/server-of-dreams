from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from models.enums import StoryEventBonusTypes


class StoryEventBonusCharacterBaseMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    story_event_master_id: int = 0
    bonus_target_type: StoryEventBonusTypes = StoryEventBonusTypes.Company
    bonus_target_id: int = 0
