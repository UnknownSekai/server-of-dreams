from __future__ import annotations

from pydantic import BaseModel


class MusicVideoOriginalCharacterMaster(BaseModel):
    order: int = 0
    character_base_master_id: int = 0
    costume_master_id: int = 0
