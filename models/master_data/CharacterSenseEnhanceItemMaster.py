from __future__ import annotations

from pydantic import BaseModel


class CharacterSenseEnhanceItemMaster(BaseModel):
    current_level: int = 0
    item_master_id: int = 0
    required_quantity: int = 0
