from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import LeagueClassTypes


class NameplateDetailMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name: Optional[str] = None
    class_type: LeagueClassTypes = LeagueClassTypes.None_
    enroll_count: int = 0
    change_value1: Optional[int] = None
    change_value2: Optional[int] = None
    priority: int = 0
