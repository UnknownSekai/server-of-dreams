from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import MusicVideoTypes


class MusicVocalVersionMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    music_master_id: int = 0
    vocal_version: int = 0
    singer: Optional[str] = None
    name: Optional[str] = None
    music_time_second: int = 0
    sample_start_seconds: float = 0.0
    sample_end_seconds: float = 0.0
    music_video_type: MusicVideoTypes = MusicVideoTypes.None_
    characters: Optional[list[int]] = None
