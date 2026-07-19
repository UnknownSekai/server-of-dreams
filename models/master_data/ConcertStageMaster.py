from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import Companies

if TYPE_CHECKING:
    from .ConcertRewardMaster import ConcertRewardMaster


class ConcertStageMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    concert_master_id: int = 0
    music_master_id: int = 0
    vocal_version: int = 0
    sense_notation_master_id: int = 0
    recommended_company: Optional[Companies] = None
    recommended_level: int = 0
    clear_score: int = 0
    rewards: Optional[list[ConcertRewardMaster]] = None
