from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class HomeCharacterVoicePeriodMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    start_month: int = 0
    start_day: int = 0
    start_time: int = 0
    end_month: int = 0
    end_day: int = 0
    end_time: int = 0
