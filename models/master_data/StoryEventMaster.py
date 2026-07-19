from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import Attributes, StoryEventCategoryTypes


class StoryEventMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    category: StoryEventCategoryTypes = StoryEventCategoryTypes.Normal
    bonus_attribute: Optional[Attributes] = None
    title: Optional[str] = None
    exchange_shop_master_id: int = 0
    event_point_item_master_id: int = 0
    start_date: str = ""
    end_date: str = ""
    force_end_date: str = ""
    bonus_category_master_id10: Optional[int] = None
    bonus_category_master_id20: Optional[int] = None
    secondary_bonus_attribute: Optional[Attributes] = None
