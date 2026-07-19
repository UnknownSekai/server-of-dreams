from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SignMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    character_base_master_id: int = 0
    sign_image_path: Optional[str] = None
