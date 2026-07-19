from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CostumeWearableCharacterGroupMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    character_base_master_ids: Optional[list[int]] = None
