from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from .RouletteRollRewardThing import RouletteRollRewardThing


class RouletteRollRewardMaster(BaseModel):
    roll_count: int = 0
    rewards: Optional[list[RouletteRollRewardThing]] = None
