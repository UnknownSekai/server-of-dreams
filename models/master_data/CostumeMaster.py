from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CostumeMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name: Optional[str] = None
    order: int = 0
    is_default: bool = False
    costume_group_master_id: int = 0
    description: Optional[str] = None
