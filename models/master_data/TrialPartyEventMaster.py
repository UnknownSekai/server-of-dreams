from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TrialPartyEventMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    m_event_id: int = 0
    is_hide_complate: bool = False
    start_date: str = ""
    end_date: str = ""
    bgm_path: Optional[str] = None
    name: Optional[str] = None
