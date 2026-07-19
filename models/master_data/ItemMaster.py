from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import ItemCategories, JumpTypes, PossessionRarities, TabCategories


class ItemMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name: Optional[str] = None
    description: Optional[str] = None
    display_order: int = 0
    display_end_date: Optional[str] = None
    max_stock: int = 0
    category: ItemCategories = ItemCategories.StaminaRecovery
    consumable: bool = False
    jump_type: Optional[JumpTypes] = None
    jump_target_id: Optional[int] = None
    tab_category: TabCategories = TabCategories.Hidden
    rarity: PossessionRarities = PossessionRarities.R
