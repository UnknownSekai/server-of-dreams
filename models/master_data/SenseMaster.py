from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import BranchConditionType, SenseTypes

if TYPE_CHECKING:
    from .BranchMaster import BranchMaster
    from .EffectOrderMaster import EffectOrderMaster


class SenseMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name: Optional[str] = None
    description: Optional[str] = None
    type: SenseTypes = SenseTypes.Support
    pre_effects: Optional[list[EffectOrderMaster]] = None
    branches: Optional[list[BranchMaster]] = None
    acquirable_gauge: int = 0
    acquirable_score_percent: int = 0
    score_up_per_level: int = 0
    light_count: int = 0
    cool_time: int = 0
    branch_condition1: BranchConditionType = BranchConditionType.None_
    condition_value1: Optional[int] = None
    branch_condition2: BranchConditionType = BranchConditionType.None_
    condition_value2: Optional[int] = None
    sub_types: Optional[list[SenseTypes]] = None
