from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import PossessionRarities


class TrophyMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name: Optional[str] = None
    description: Optional[str] = None
    rarity: PossessionRarities = PossessionRarities.R
    order: int = 0
    trophy_group_master_id: int = 0
    hidden: bool = False
    unlock_text: Optional[str] = None
