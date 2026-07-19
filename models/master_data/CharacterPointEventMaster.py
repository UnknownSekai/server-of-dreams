from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CharacterPointEventMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    event_master_id: int = 0
    title: Optional[str] = None
    exchange_shop_master_id: int = 0
    event_point_item_master_id: int = 0
    character_base_master_ids: Optional[list[int]] = None
