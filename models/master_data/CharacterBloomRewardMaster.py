from __future__ import annotations

from pydantic import BaseModel

from models.enums import ThingTypes


class CharacterBloomRewardMaster(BaseModel):
    thing_id: int = 0
    thing_type: ThingTypes = ThingTypes.Item
    thing_quantity: int = 0
    phase: int = 0
