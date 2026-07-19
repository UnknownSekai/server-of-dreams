from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class PlayerRankMaster(BaseModel):
    rank: int = 0
    point_to_level_up: int = 0
    max_stamina: int = 0
    is_released_rank: bool = False
    player_rank_cap_master_id: Optional[int] = None
