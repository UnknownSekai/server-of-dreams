from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AlbumEffectMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    level: int = 0
    description: Optional[str] = None
    effect_master_id: int = 0
