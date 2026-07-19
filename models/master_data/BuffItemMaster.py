from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import CampaignEffectTypes


class BuffItemMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    item_master_id: int = 0
    effect_type: CampaignEffectTypes = CampaignEffectTypes.LiveReward
    effect_value: int = 0
    valid_day: int = 0
    dialog_title: Optional[str] = None
    dialog_description: Optional[str] = None
