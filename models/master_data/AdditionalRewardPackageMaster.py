from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .AdditionalRewardThingMaster import AdditionalRewardThingMaster


class AdditionalRewardPackageMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    description: Optional[str] = None
    live_setting_master_id: int = 0
    rewards: Optional[list[AdditionalRewardThingMaster]] = None
    etcetera: bool = False
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    order: int = 0
