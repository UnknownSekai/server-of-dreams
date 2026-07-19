from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .TrialPartyEventStageRewardMaster import TrialPartyEventStageRewardMaster


class TrialPartyEventStageMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    trial_party_event_master_id: int = 0
    music_master_id: int = 0
    vocal_version: int = 0
    sense_notation_master_id: int = 0
    clear_score: int = 0
    clear_sense_count: int = 0
    clear_star_act_count: int = 0
    clear_principal_gauge_value: int = 0
    title: Optional[str] = None
    hint: Optional[str] = None
    restriction_info: Optional[str] = None
    rewards: Optional[list[TrialPartyEventStageRewardMaster]] = None
    trial_party_master_id: int = 0
    unrecommended_auto: bool = False
