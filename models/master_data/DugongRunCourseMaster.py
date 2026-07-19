from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import DugongRunDifficultyTypes


class DugongRunCourseMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    event_master_id: Optional[int] = None
    difficulty: DugongRunDifficultyTypes = DugongRunDifficultyTypes.Easy
    music_master_id: int = 0
    notation_path: Optional[str] = None
    scroll_speed: int = 0
    dugong_run_course_group_id: int = 0
