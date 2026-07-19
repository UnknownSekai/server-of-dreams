from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import SpotTypes


class SpotConversationMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    spot: SpotTypes = SpotTypes.UtagawaHighSchool
    character_id1: Optional[int] = None
    character_id2: Optional[int] = None
    character_id3: Optional[int] = None
    character_id4: Optional[int] = None
    character_id5: Optional[int] = None
    episode_master_id: int = 0
    costume_id1: Optional[int] = None
    costume_id2: Optional[int] = None
    costume_id3: Optional[int] = None
    costume_id4: Optional[int] = None
    costume_id5: Optional[int] = None
    title: Optional[str] = None
