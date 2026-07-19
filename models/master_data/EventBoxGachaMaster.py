from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .EventBoxGachaDetailMaster import EventBoxGachaDetailMaster


class EventBoxGachaMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name: Optional[str] = None
    event_master_id: int = 0
    required_item_master_id: int = 0
    required_quantity: int = 0
    details: Optional[list[EventBoxGachaDetailMaster]] = None
    event_box_gacha_text_template_master_id: int = 0
