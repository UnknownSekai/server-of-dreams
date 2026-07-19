from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class EventBoxGachaDetailMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    order: int = 0
    prize_count: int = 0
