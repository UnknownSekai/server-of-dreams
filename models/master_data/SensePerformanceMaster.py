from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .SensePerformanceCharacterMaster import SensePerformanceCharacterMaster


class SensePerformanceMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    label_type: int = 0
    performance_group: Optional[int] = None
    characters: Optional[list[SensePerformanceCharacterMaster]] = None
