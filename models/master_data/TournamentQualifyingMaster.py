from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TournamentQualifyingMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    event_master_id: int = 0
    entry_page_url: Optional[str] = None
    entry_start_date: str = ""
    entry_end_date: str = ""
    website_url: Optional[str] = None
