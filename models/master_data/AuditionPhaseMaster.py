from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AuditionPhaseMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    auditionaster_id: int = 0
    phase: int = 0
    recommended_player_rank: int = 0
    clear_score: int = 0
    star_act_count: Optional[int] = None
    audition_reward_package_master_id: int = 0
