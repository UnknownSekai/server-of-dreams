from __future__ import annotations

from pydantic import BaseModel


class EffectDetailMaster(BaseModel):
    level: int = 0
    value: float = 0.0
