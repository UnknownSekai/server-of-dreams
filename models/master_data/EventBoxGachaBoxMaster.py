from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .EventBoxGachaBoxThingMaster import EventBoxGachaBoxThingMaster


class EventBoxGachaBoxMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    event_box_gacha_master_id: int = 0
    order: int = 0
    box_things: Optional[list[EventBoxGachaBoxThingMaster]] = None
