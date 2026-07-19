from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TipMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    character_base_master_id: int = 0
    description: Optional[str] = None
    name: Optional[str] = None
