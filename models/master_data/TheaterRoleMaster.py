from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class TheaterRoleMaster(BaseModel):
    role_name: Optional[str] = None
    character_base_master_id: int = 0
    costume_master_id: int = 0
    order: int = 0
