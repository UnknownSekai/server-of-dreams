from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from models.enums import MusicDifficulties


class LeagueMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    music_master_id: int = 0
    max_difficulty: MusicDifficulties = MusicDifficulties.None_
    display_start_at: str = ""
    counting_start_at: str = ""
    display_end_at: str = ""
    league_class_group_master_id: int = 0
    sense_notation_master_id: int = 0
    vocal_version: int = 0
    league_season_master_id: int = 0
