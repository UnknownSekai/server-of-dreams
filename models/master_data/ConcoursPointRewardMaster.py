from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .ConcoursPointRewardThingMaster import ConcoursPointRewardThingMaster


class ConcoursPointRewardMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    concours_master_id: int = 0
    required_point: int = 0
    things: Optional[list[ConcoursPointRewardThingMaster]] = None
