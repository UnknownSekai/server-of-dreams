from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ConcertMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    start_date: str = ""
    end_date: str = ""
    name: Optional[str] = None
    event_master_id: int = 0
