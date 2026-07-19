from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CostumeGroupMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name: Optional[str] = None
    description: Optional[str] = None
    order: int = 0
    costume_master_ids: Optional[list[int]] = None
    costume_wearable_character_group_master_id: Optional[int] = None
    performance_group_id: Optional[int] = None
    is_hair_change: bool = False
    display_start_at: str = ""
    display_end_at: str = ""
