from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from models.enums import CharacterEpisodeOrder


class CharacterEpisodeMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    character_master_id: int = 0
    episode_master_id: int = 0
    episode_order: CharacterEpisodeOrder = CharacterEpisodeOrder.None_
    required_character_level: int = 0
