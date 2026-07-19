from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class FilmItemMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    item_master_id: int = 0
    target_character_base_master_id: Optional[int] = None
