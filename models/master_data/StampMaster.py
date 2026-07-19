from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import StampType


class StampMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    order: int = 0
    is_default: bool = False
    character_base_master_id: int = 0
    type: StampType = StampType.Default
    asset_id: Optional[str] = None
    voice_asset_id: Optional[str] = None
    name: Optional[str] = None
    character_base_master_ids: Optional[list[int]] = None
