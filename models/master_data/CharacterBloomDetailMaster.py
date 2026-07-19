from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class CharacterBloomDetailMaster(BaseModel):
    character_master_id: int = 0
    text: Optional[str] = None
    voice_path: Optional[str] = None
