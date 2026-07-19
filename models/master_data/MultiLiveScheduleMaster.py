from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import LiveScheduleEndDateDisplayType


class MultiLiveScheduleMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    start_date: str = ""
    end_date: str = ""
    live_setting_master_id1: int = 0
    live_setting_master_id2: int = 0
    additional_end_date: Optional[str] = None
    end_date_display_type1: LiveScheduleEndDateDisplayType = (
        LiveScheduleEndDateDisplayType.None_
    )
    end_date_display_type2: LiveScheduleEndDateDisplayType = (
        LiveScheduleEndDateDisplayType.None_
    )
