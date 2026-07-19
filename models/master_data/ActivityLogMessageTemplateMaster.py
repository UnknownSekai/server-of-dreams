from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import ActivityLogTypes


class ActivityLogMessageTemplateMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    log_type: ActivityLogTypes = ActivityLogTypes.None_
    message_template: Optional[str] = None
