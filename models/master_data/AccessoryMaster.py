from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import PossessionRarities


class AccessoryMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name: Optional[str] = None
    description: Optional[str] = None
    rarity: PossessionRarities = PossessionRarities.R
    accessory_level_pattern_group_id: int = 0
    fixed_accessory_effects: Optional[list[int]] = None
    random_effect_groups: Optional[list[int]] = None
    pronounce_name: Optional[str] = None
    series: int = 0
    max_level: int = 0
