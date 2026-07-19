from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import Companies


class CircleSupportCompanyLevelDetailMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    company: Companies = Companies.None_
    level: int = 0
    required_support_point: int = 0
    effect_master_id: int = 0
    description: Optional[str] = None
    release_date: str = ""
