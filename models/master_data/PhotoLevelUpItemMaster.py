from __future__ import annotations

from pydantic import BaseModel


class PhotoLevelUpItemMaster(BaseModel):
    item_master_id: int = 0
    required_quantity: int = 0
