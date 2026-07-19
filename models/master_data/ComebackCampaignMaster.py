from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ComebackCampaignMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    mission_active_days: int = 0
    jewel_shop_item_active_days: int = 0
    login_bonus_active_days: int = 0
    buff_campaign_active_days: int = 0
