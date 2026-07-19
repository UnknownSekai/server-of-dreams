from __future__ import annotations

from pydantic import BaseModel


class CharacterLevelMaster(BaseModel):
    level: int = 0
    experience_to_level_up: int = 0
    character_status_level: int = 0
    start_date: str = ""
