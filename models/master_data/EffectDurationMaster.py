from __future__ import annotations

from pydantic import BaseModel


class EffectDurationMaster(BaseModel):
    level: int = 0
    duration_seconds: float = 0.0
