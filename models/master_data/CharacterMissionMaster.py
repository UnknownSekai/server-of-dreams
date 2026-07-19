from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import JumpTypes

if TYPE_CHECKING:
    from .CharacterMissionStageMaster import CharacterMissionStageMaster


class CharacterMissionMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    title: Optional[str] = None
    jump_type: Optional[JumpTypes] = None
    jump_value: Optional[int] = None
    stages: Optional[list[CharacterMissionStageMaster]] = None
