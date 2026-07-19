from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from .LeaderSenseDetailConditionMaster import LeaderSenseDetailConditionMaster


class LeaderSenseDetailMaster(BaseModel):
    effect_master_id: int = 0
    conditions: Optional[list[LeaderSenseDetailConditionMaster]] = None
