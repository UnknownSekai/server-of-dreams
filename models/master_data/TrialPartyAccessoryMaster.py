from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TrialPartyAccessoryMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    trial_party_master_id: int = 0
    accessory_master_id: int = 0
    level: int = 0
    accessory_effects: Optional[list[int]] = None
