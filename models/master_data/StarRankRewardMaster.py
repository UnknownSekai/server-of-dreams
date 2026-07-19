from __future__ import annotations

from pydantic import BaseModel


class StarRankRewardMaster(BaseModel):
    rank: int = 0
    character_base_master_id: int = 0
    character_star_rank_reward_group_master_id: int = 0
