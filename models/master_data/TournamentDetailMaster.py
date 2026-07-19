from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from models.enums import MusicDifficulties


class TournamentDetailMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    music_master_id: int = 0
    difficulty: MusicDifficulties = MusicDifficulties.None_
