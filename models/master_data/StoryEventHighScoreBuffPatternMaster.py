from __future__ import annotations

from pydantic import BaseModel


class StoryEventHighScoreBuffPatternMaster(BaseModel):
    next_level: int = 0
    required_point: int = 0
