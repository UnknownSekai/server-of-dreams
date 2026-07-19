from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import RouletteTypes

if TYPE_CHECKING:
    from .RoulettePrizeMaster import RoulettePrizeMaster
    from .RouletteRollRewardMaster import RouletteRollRewardMaster


class RouletteMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    roulette_event_master_id: int = 0
    order: int = 0
    roulette_type: RouletteTypes = RouletteTypes.Point
    roulette_ticket_item_master_id: int = 0
    required_ticket_quantity: int = 0
    roulette_image_path: Optional[str] = None
    prizes: Optional[list[RoulettePrizeMaster]] = None
    roll_rewards: Optional[list[RouletteRollRewardMaster]] = None
    name: Optional[str] = None
