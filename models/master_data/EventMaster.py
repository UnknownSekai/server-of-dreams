from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import AsideLiveButtonTypes, Attributes, EventTypes

if TYPE_CHECKING:
    from .EventBonusMaster import EventBonusMaster
    from .EventPointRewardMaster import EventPointRewardMaster
    from .EventRankingRewardMaster import EventRankingRewardMaster


class EventMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    event_type: EventTypes = EventTypes.StoryEvent
    start_date: str = ""
    end_date: str = ""
    force_end_date: str = ""
    name: Optional[str] = None
    is_aside_live_button: bool = False
    event_point_item_master_id: Optional[int] = None
    bonus_attribute: Optional[Attributes] = None
    bonus_category_master_id10: Optional[int] = None
    bonus_category_master_id20: Optional[int] = None
    bonuses: Optional[list[EventBonusMaster]] = None
    point_rewards: Optional[list[EventPointRewardMaster]] = None
    ranking_rewards: Optional[list[EventRankingRewardMaster]] = None
    exchange_shop_master_id: Optional[int] = None
    aside_live_button_type: AsideLiveButtonTypes = AsideLiveButtonTypes.None_
    secondary_bonus_attribute: Optional[Attributes] = None
