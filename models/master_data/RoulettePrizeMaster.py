from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .RoulettePrizeThingMaster import RoulettePrizeThingMaster


class RoulettePrizeMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    slot: int = 0
    acquire_point_quantity: Optional[int] = None
    acquire_prize_thing: Optional[RoulettePrizeThingMaster] = None
