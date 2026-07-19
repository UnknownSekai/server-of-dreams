from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import ConditionUsableTableFilter, UnlockConditionTypes


class UnlockConditionMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    condition_text: Optional[str] = None
    condition_usable_table_filter: ConditionUsableTableFilter = (
        ConditionUsableTableFilter.DisplayRestriction
    )
    unlock_condition_type: UnlockConditionTypes = UnlockConditionTypes.CharacterStarRank
