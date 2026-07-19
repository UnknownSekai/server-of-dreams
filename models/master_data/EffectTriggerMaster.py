from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from models.enums import TriggerType


class EffectTriggerMaster(BaseModel):
    trigger: TriggerType = TriggerType.OverLife
    value: Optional[int] = None
