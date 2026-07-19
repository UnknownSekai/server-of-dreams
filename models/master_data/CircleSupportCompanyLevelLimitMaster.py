from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .CircleSupportCompanyLevelLimitDetailMaster import (
        CircleSupportCompanyLevelLimitDetailMaster,
    )


class CircleSupportCompanyLevelLimitMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    next_level_limit: int = 0
    required_coin: int = 0
    release_date: str = ""
    details: Optional[list[CircleSupportCompanyLevelLimitDetailMaster]] = None
