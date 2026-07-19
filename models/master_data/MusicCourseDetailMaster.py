from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import MusicDifficulties


class MusicCourseDetailMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    set_list_number: int = 0
    live_master_id: Optional[int] = None
    vocal_version: int = 0
    another_notation_master_id: int = 0
    random_difficulty: Optional[MusicDifficulties] = None
    random_level: Optional[int] = None
