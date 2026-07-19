from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import AnotherNotationTypes, MusicDifficulties


class AnotherNotationMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    music_master_id: int = 0
    vocal_version: int = 0
    notation_path: Optional[str] = None
    difficulty: MusicDifficulties = MusicDifficulties.None_
    level: int = 0
    another_notation_type: AnotherNotationTypes = AnotherNotationTypes.Shelved
    start_date: str = ""
    end_date: str = ""
