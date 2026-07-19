from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .CircleEventMissionRefreshSetting import CircleEventMissionRefreshSetting


class CircleEventMissionRefreshSettingGroupMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    settings: Optional[list[CircleEventMissionRefreshSetting]] = None
