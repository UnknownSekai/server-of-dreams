from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from models.enums import TitleCallVoicePriorityTypes


class TitleCallVoiceMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    priority: TitleCallVoicePriorityTypes = TitleCallVoicePriorityTypes.Normal
    voice_id: int = 0
    start_date: str = ""
    end_date: str = ""
