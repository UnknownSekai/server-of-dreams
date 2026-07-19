from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import HomeBGMPriorityTypes, HomeBGMSelectionTypes


class HomeBGMMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    priority: HomeBGMPriorityTypes = HomeBGMPriorityTypes.Normal
    selection_type: HomeBGMSelectionTypes = HomeBGMSelectionTypes.UserSelect
    default_bgm_name: Optional[str] = None
    default_bgm_path: Optional[str] = None
    start_date: str = ""
    end_date: str = ""
