from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .GradualMissionMaster import GradualMissionMaster


class GradualMissionGroupMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    start_date: str = ""
    end_date: str = ""
    missions: Optional[list[GradualMissionMaster]] = None
