from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import BranchConditionType, PosterEffectTypes

if TYPE_CHECKING:
    from .BranchMaster import BranchMaster


class PosterAbilityMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name: Optional[str] = None
    description: Optional[str] = None
    poster_master_id: int = 0
    type: PosterEffectTypes = PosterEffectTypes.Leader
    frame_number: int = 0
    release_level_at: int = 0
    hidden: bool = False
    branches: Optional[list[BranchMaster]] = None
    branch_condition_type1: BranchConditionType = BranchConditionType.None_
    condition_value1: Optional[int] = None
    branch_condition_type2: BranchConditionType = BranchConditionType.None_
    condition_value2: Optional[int] = None
