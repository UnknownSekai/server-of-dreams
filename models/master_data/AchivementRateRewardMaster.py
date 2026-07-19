from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from models.enums import MusicDifficulties, ThingTypes


class AchivementRateRewardMaster(BaseModel):
    thing_type: ThingTypes = ThingTypes.Item
    thing_id: int = 0
    thing_quantity: int = 0
    difficulty: MusicDifficulties = MusicDifficulties.None_
    achivement_rate: Optional[str] = None
