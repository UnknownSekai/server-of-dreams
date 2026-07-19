from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class HomeSkinMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name: Optional[str] = None
    order: int = 0
    unlock_condition_text: Optional[str] = None
    hidden: bool = False
    is_default: bool = False
    display_start_date: Optional[str] = None
