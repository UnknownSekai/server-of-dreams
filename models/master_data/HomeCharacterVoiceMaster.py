from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class HomeCharacterVoiceMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    character_base_master_id: int = 0
    text: Optional[str] = None
    weight: int = 0
    character_voice_period_master_id: Optional[int] = None
    is_player_birth_date_voice: bool = False
    voice_file_name1: Optional[str] = None
    voice_file_name2: Optional[str] = None
    voice_file_name3: Optional[str] = None
    voice_file_name4: Optional[str] = None
    voice_interval1: float = 0.0
    voice_interval2: float = 0.0
    voice_interval3: float = 0.0
    mouth_motion_id1: Optional[str] = None
    mouth_motion_id2: Optional[str] = None
    mouth_motion_id3: Optional[str] = None
    mouth_motion_id4: Optional[str] = None
    body_motion_id1: Optional[str] = None
    body_motion_id2: Optional[str] = None
    body_motion_id3: Optional[str] = None
    body_motion_id4: Optional[str] = None
