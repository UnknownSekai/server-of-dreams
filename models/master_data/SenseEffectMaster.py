from __future__ import annotations

from pydantic import BaseModel


class SenseEffectMaster(BaseModel):
    order: int = 0
    effect_master_id: int = 0
