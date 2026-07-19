from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import BonusLiveUnlockConditionTypes

if TYPE_CHECKING:
    from .BonusLiveStageMaster import BonusLiveStageMaster


class BonusLiveMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    event_master_id: int = 0
    first_clear_event_point_quantity: int = 0
    clear_event_point_quantity: int = 0
    unlock_condition_type: BonusLiveUnlockConditionTypes = (
        BonusLiveUnlockConditionTypes.RouletteEventPoint
    )
    unlock_condition_value: Optional[int] = None
    stages: Optional[list[BonusLiveStageMaster]] = None
