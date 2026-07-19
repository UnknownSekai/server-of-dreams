from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .StoryEventRewardThing import StoryEventRewardThing


class StoryEventRewardItemPackage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    rewards: Optional[list[StoryEventRewardThing]] = None
