from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class EventCampMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    event_master_id: int = 0
    win_camp_ratio: int = 0
    lose_camp_ratio: int = 0
    none_camp_ratio: int = 0
    camp1_team_name: Optional[str] = None
    camp2_team_name: Optional[str] = None
    camp_select_message: Optional[str] = None
    bgm_path: Optional[str] = None
    character_master_id_icon_left: int = 0
    character_master_id_icon_right: int = 0
