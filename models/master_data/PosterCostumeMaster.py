from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class PosterCostumeMaster(BaseModel):
    phase: int = 0
    costume_master_id: Optional[int] = None
    item_master_id: Optional[int] = None
    quantity: int = 0
    decoration_master_id: Optional[int] = None
