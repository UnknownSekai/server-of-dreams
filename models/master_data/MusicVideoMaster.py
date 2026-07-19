from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .MusicVideoOriginalCharacterMaster import MusicVideoOriginalCharacterMaster


class MusicVideoMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    music_master_id: int = 0
    member_amount: int = 0
    display_start_at: str = ""
    display_end_at: Optional[str] = None
    characters: Optional[list[MusicVideoOriginalCharacterMaster]] = None
    delay_seconds: float = 0.0
    movie_delay_seconds: float = 0.0
    music_video_default_costume_group_master_id: Optional[int] = None
    is_fixed_member: bool = False
    order: int = 0
