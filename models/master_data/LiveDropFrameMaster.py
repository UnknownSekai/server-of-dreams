from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import FrameLotConditionTypes, ProbabilityChangeTypes

if TYPE_CHECKING:
    from .LiveDropThingMaster import LiveDropThingMaster


class LiveDropFrameMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    live_drop_frame_group_master_id: int = 0
    order: int = 0
    change_type: ProbabilityChangeTypes = ProbabilityChangeTypes.None_
    frame_lot_condition: FrameLotConditionTypes = FrameLotConditionTypes.None_
    unaffected_increase_effect: bool = False
    rewards: Optional[list[LiveDropThingMaster]] = None
    frame_lot_condition_value: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
