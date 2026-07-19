from __future__ import annotations

from pydantic import BaseModel


class CircleEventMissionRefreshSetting(BaseModel):
    min_refresh_count: int = 0
    max_refresh_count: int = 0
    required_coin: int = 0
