from __future__ import annotations

from pydantic import BaseModel


class StepupGachaMaster(BaseModel):
    gacha_master_id: int = 0
    step: int = 0
