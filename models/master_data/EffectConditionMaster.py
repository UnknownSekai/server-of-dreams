from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from models.enums import EffectConditions


class EffectConditionMaster(BaseModel):
    condition: EffectConditions = EffectConditions.CharacterBase
    value: Optional[int] = None
