from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import JumpTypes, MissionCategories

if TYPE_CHECKING:
    from .MissionStageMaster import MissionStageMaster


class MissionMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    mission_category: MissionCategories = MissionCategories.Beginner
    mission_view_order: int = 0
    title: Optional[str] = None
    description: Optional[str] = None
    event_master_id: Optional[int] = None
    jump_type: JumpTypes = JumpTypes.None_
    jump_target_id: Optional[int] = None
    start_date: str = ""
    end_date: str = ""
    stages: Optional[list[MissionStageMaster]] = None
    comeback_campaign_master_id: Optional[int] = None
