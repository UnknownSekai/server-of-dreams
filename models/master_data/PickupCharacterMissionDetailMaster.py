from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import PickupCharacterMissionCheckCondition

if TYPE_CHECKING:
    from .PickupCharacterMissionDetailRewardMaster import (
        PickupCharacterMissionDetailRewardMaster,
    )


class PickupCharacterMissionDetailMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    order: int = 0
    check_condition: PickupCharacterMissionCheckCondition = (
        PickupCharacterMissionCheckCondition.Level
    )
    description: Optional[str] = None
    goal_value: int = 0
    rewards: Optional[list[PickupCharacterMissionDetailRewardMaster]] = None
