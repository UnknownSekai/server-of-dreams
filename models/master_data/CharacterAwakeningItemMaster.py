from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class CharacterAwakeningItemMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    awakening_phase: int = 0
    item_master_id: int = 0
    required_quantity: int = 0
