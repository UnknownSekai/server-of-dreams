from __future__ import annotations

from pydantic import BaseModel


class CharacterCategoryMaster(BaseModel):
    category_master_id: int = 0
    is_awaken: bool = False
