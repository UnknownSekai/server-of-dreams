from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import LeagueClassTypes

if TYPE_CHECKING:
    from .TripleCastGroupRankingRewardThingMaster import (
        TripleCastGroupRankingRewardThingMaster,
    )


class TripleCastGroupRankingRewardPackageMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    rewards: Optional[list[TripleCastGroupRankingRewardThingMaster]] = None
    class_type: LeagueClassTypes = LeagueClassTypes.None_
    min_rank: int = 0
    max_rank: int = 0
    reward_title: Optional[str] = None
