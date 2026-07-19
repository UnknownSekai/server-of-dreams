from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from models.enums import CharacterEpisodeOrder


class TrialPartyCharacterMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    trial_party_master_id: int = 0
    character_master_id: int = 0
    level: int = 0
    talent_stage: int = 0
    awakening_status: int = 0
    sense_level: int = 0
    read_episode_order: CharacterEpisodeOrder = CharacterEpisodeOrder.None_
