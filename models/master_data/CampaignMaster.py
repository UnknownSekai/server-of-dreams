from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import CampaignEffectTypes


class CampaignMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    title: Optional[str] = None
    description: Optional[str] = None
    icon_image_path: Optional[str] = None
    order: int = 0
    start_date: str = ""
    end_date: str = ""
    comeback_campaign_master_id: Optional[int] = None
    campaign_effect_type: CampaignEffectTypes = CampaignEffectTypes.LiveReward
    campaign_effect_value: int = 0
