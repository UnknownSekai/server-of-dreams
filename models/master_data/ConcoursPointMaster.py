from __future__ import annotations

from pydantic import BaseModel


class ConcoursPointMaster(BaseModel):
    target_highest_rank: int = 0
    target_lowest_rank: int = 0
    point: int = 0
