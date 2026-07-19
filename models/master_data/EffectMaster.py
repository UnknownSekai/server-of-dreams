from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import (
    CalculationTypes,
    EffectTargetRanges,
    EffectTypes,
    FireTimingTypes,
)

if TYPE_CHECKING:
    from .EffectConditionMaster import EffectConditionMaster
    from .EffectDetailMaster import EffectDetailMaster
    from .EffectTriggerMaster import EffectTriggerMaster


class EffectMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    type: EffectTypes = EffectTypes.BaseVocalUp
    range: EffectTargetRanges = EffectTargetRanges.None_
    calculation_type: CalculationTypes = CalculationTypes.PercentageAddition
    details: Optional[list[EffectDetailMaster]] = None
    conditions: Optional[list[EffectConditionMaster]] = None
    duration_second: int = 0
    triggers: Optional[list[EffectTriggerMaster]] = None
    fire_timing_type: FireTimingTypes = FireTimingTypes.StarAct
