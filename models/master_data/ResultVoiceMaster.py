from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import ResultVoiceConditionTypes


class ResultVoiceMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    character_base_master_id: int = 0
    order: int = 0
    condition_type: ResultVoiceConditionTypes = ResultVoiceConditionTypes.AllPerfect
    voice_asset_id: Optional[str] = None
    motion: Optional[str] = None
