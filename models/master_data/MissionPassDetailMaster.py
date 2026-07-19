from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .MissionPassRewardThing import MissionPassRewardThing


class MissionPassDetailMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    phase: int = 0
    mission_pass_master_id: Optional[int] = None
    clear_point: int = 0
    start_date: str = ""
    end_date: str = ""
    rewards: Optional[list[MissionPassRewardThing]] = None
