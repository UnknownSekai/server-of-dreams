from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .StepupGachaMaster import StepupGachaMaster


class StepupGachaGroupMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    stepup_gachas: Optional[list[StepupGachaMaster]] = None
