from __future__ import annotations

from pydantic import BaseModel


class PlayerRankCapDetailMaster(BaseModel):
    item_master_id: int = 0
    quantity: int = 0
