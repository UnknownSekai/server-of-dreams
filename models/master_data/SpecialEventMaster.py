from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import SpecialEventCategoryTypes

if TYPE_CHECKING:
    from .EventMaster import EventMaster
    from .SpecialEventLayout import SpecialEventLayout


class SpecialEventMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    event_master: Optional[EventMaster] = None
    event_name: Optional[str] = None
    category_type: SpecialEventCategoryTypes = SpecialEventCategoryTypes.TotalPoint
    layouts: Optional[list[SpecialEventLayout]] = None
    game_hint_page_count: int = 0
