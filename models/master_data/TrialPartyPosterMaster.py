from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class TrialPartyPosterMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    trial_party_master_id: int = 0
    poster_master_id: int = 0
    level: int = 0
    breakthrough_phase: int = 0
