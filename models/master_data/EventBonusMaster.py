from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from models.enums import StoryEventBonusTypes


class EventBonusMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    bonus_target_type: StoryEventBonusTypes = StoryEventBonusTypes.Company
    bonus_target_id: int = 0
