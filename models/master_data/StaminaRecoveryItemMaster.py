from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class StaminaRecoveryItemMaster(BaseModel):
    item_master_id: int = 0
    recovery_amount: int = 0
    expired_at: Optional[str] = None
    is_force_show_list: bool = False
