from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class HomePosterMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    poster_master_id: int = 0
    gacha_master_id: Optional[int] = None
    display_start_date: str = ""
    display_end_date: str = ""
