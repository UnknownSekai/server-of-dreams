from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import Companies


class AuditionMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    music_master_id: int = 0
    recommended_company: Companies = Companies.None_
    can_skip: bool = False
    sense_notation_master_id: int = 0
    max_phase: Optional[str] = None
    display_start_at: str = ""
    display_end_at: str = ""
    vocal_version: int = 0
    audition_group_number: int = 0
    skip_start_at: str = ""
