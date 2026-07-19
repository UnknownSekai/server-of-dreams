from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class NameColorMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name: Optional[str] = None
    description: Optional[str] = None
    order: int = 0
    hidden: bool = False
    is_default: bool = False
    unlock_text: Optional[str] = None
