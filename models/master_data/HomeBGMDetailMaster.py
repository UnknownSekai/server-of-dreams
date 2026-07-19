from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class HomeBGMDetailMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    home_bgm_master_id: int = 0
    bgm_name: Optional[str] = None
    bgm_path: Optional[str] = None
    start_date: str = ""
    end_date: str = ""
    music_master_id: int = 0
