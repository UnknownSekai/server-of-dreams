from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class TimeLimitedControlMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    end_date: str = ""
