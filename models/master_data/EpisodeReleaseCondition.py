from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from models.enums import EpisodeReleaseConditionTypes


class EpisodeReleaseCondition(BaseModel):
    condition_type: EpisodeReleaseConditionTypes = (
        EpisodeReleaseConditionTypes.TotalRankInCompany
    )
    value1: Optional[int] = None
    value2: Optional[int] = None
    value3: Optional[int] = None
