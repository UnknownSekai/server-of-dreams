from __future__ import annotations

from pydantic import BaseModel


class CharacterEpisodeReleaseItemMaster(BaseModel):
    item_master_id: int = 0
    required_quantity: int = 0
    order: int = 0
