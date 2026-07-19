from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import BranchJudgeTypes

if TYPE_CHECKING:
    from .EffectOrderMaster import EffectOrderMaster


class BranchMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    order: int = 0
    branch_effects: Optional[list[EffectOrderMaster]] = None
    judge_type1: Optional[BranchJudgeTypes] = None
    parameter1: Optional[int] = None
    judge_type2: Optional[BranchJudgeTypes] = None
    parameter2: Optional[int] = None
    id_: int = Field(default=0, alias="id")
