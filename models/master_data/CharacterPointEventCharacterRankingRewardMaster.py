from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class CharacterPointEventCharacterRankingRewardMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    character_point_event_master_id: int = 0
    character_base_master_id: int = 0
    target_min_rank: int = 0
    target_max_rank: int = 0
    character_point_event_character_ranking_reward_item_package_master_id: int = 0
