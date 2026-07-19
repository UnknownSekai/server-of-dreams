from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import BranchConditionType

if TYPE_CHECKING:
    from .BranchMaster import BranchMaster
    from .EffectOrderMaster import EffectOrderMaster


class StarActMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name: Optional[str] = None
    description: Optional[str] = None
    star_act_condition_master_id: int = 0
    acquirable_score_percent: int = 0
    score_up_per_level: int = 0
    pre_effects: Optional[list[EffectOrderMaster]] = None
    branches: Optional[list[BranchMaster]] = None
    branch_condition1: BranchConditionType = BranchConditionType.None_
    condition_value1: Optional[int] = None
    branch_condition2: BranchConditionType = BranchConditionType.None_
    condition_value2: Optional[int] = None
