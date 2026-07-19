from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import LeagueClassTypes


class LeagueClassMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    up_user_amount: Optional[int] = None
    keep_user_amount: Optional[int] = None
    is_force_down_not_playing_league: bool = False
    up_reward_package_master_id: Optional[int] = None
    keep_reward_package_master_id: Optional[int] = None
    down_reward_package_master_id: Optional[int] = None
    first_achieve_reward_package_master_id: Optional[int] = None
    nameplate_master_id: Optional[int] = None
    class_type: LeagueClassTypes = LeagueClassTypes.None_
    league_class_group_master_id: int = 0
