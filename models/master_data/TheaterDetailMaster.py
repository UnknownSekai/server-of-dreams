from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TheaterDetailMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    speaker: Optional[str] = None
    phrase: Optional[str] = None
    voice_asset_id: Optional[str] = None
