from __future__ import annotations

from pydantic import BaseModel

from models.enums import ThingTypes


class CharacterStarRankRewardMaster(BaseModel):
    thing_type: ThingTypes = ThingTypes.Item
    thing_id: int = 0
    thing_quantity: int = 0
