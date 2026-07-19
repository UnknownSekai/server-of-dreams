from __future__ import annotations

from pydantic import BaseModel


class CharacterStarRankMaster(BaseModel):
    rank: int = 0
    next_rank_point: int = 0
    required_lesson_score: int = 0
    status_bonus: float = 0.0
