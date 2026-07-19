from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import LiveUnlockConditionTypes, MusicDifficulties


class LiveMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    difficulty: MusicDifficulties = MusicDifficulties.None_
    music_master_id: int = 0
    level: int = 0
    note_count: int = 0
    unlock_condition: LiveUnlockConditionTypes = LiveUnlockConditionTypes.None_
    unlock_value: Optional[int] = None
    start_date: str = ""
    end_date: str = ""
