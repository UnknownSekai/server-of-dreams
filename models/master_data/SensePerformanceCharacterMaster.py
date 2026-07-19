from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SensePerformanceCharacterMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    character_base_master_id: int = 0
    sense_performance_master_id: int = 0
    express_id: Optional[str] = None
