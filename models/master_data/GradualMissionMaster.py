from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class GradualMissionMaster(BaseModel):
    days: int = 0
    mission_master_ids: Optional[list[int]] = None
