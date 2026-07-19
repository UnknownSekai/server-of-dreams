from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class SenseNotationDetailMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    position: int = 0
    timing_second: int = 0
