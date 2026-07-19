from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .TripleCastAllClassGlobalRankingRewardThingMaster import (
        TripleCastAllClassGlobalRankingRewardThingMaster,
    )


class TripleCastAllClassGlobalRankingRewardPackageMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    triple_cast_master_id: int = 0
    rewards: Optional[list[TripleCastAllClassGlobalRankingRewardThingMaster]] = None
    min_rank: int = 0
    max_rank: int = 0
    reward_title: Optional[str] = None
