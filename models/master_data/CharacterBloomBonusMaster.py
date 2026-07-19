from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from models.enums import BloomBonusTypes


class CharacterBloomBonusMaster(BaseModel):
    bloom_bonus_type: BloomBonusTypes = BloomBonusTypes.None_
    description: Optional[str] = None
    phase: int = 0
    effect_master_id: int = 0
    icon_path: Optional[str] = None
