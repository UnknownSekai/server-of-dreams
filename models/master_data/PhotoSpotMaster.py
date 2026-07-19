from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PhotoSpotMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name: Optional[str] = None
    release_player_rank: int = 0
    display_start_at: str = ""
    display_end_at: str = ""
