from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import MusicCoverTypes, MusicUnlockConditionTypes, MusicVideoTypes

if TYPE_CHECKING:
    from .MusicVocalVersionMaster import MusicVocalVersionMaster


class MusicMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name: Optional[str] = None
    description: Optional[str] = None
    reward_rule_master_id: int = 0
    pronounce_name: Optional[str] = None
    lyric_writer: Optional[str] = None
    composer: Optional[str] = None
    arranger: Optional[str] = None
    unlock_text: Optional[str] = None
    is_long_version: bool = False
    released_at: Optional[str] = None
    stamina_consumption: int = 0
    music_time_second: int = 0
    invisible: bool = False
    sample_start_seconds: float = 0.0
    sample_end_seconds: float = 0.0
    delay_seconds: float = 0.0
    vocal_versions: Optional[list[MusicVocalVersionMaster]] = None
    unlock_condition_type: MusicUnlockConditionTypes = MusicUnlockConditionTypes.Default
    unlock_condition_value: Optional[int] = None
    music_video_type: MusicVideoTypes = MusicVideoTypes.None_
    music_cover_type: MusicCoverTypes = MusicCoverTypes.Original
    story_event_master_id: Optional[int] = None
    story_master_id: Optional[int] = None
    event_master_id: Optional[int] = None
