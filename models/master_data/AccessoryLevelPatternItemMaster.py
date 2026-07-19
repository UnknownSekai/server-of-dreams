from __future__ import annotations

from pydantic import BaseModel


class AccessoryLevelPatternItemMaster(BaseModel):
    item_master_id: int = 0
    quantity: int = 0
