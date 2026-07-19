from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import LiveTypes


class LiveSettingMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name: Optional[str] = None
    live_type: LiveTypes = LiveTypes.Normal
    live_drop_frame_group_master_id: int = 0
