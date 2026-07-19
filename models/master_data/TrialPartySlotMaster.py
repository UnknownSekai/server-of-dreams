from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from models.enums import TrialPartyCharacterLockTypes, TrialPartyEquipmentLockTypes


class TrialPartySlotMaster(BaseModel):
    position: int = 0
    is_position_lock: bool = False
    trial_party_character_master_id: int = 0
    character_lock_type: TrialPartyCharacterLockTypes = (
        TrialPartyCharacterLockTypes.None_
    )
    trial_party_poster_master_id: Optional[int] = None
    poster_lockype: TrialPartyEquipmentLockTypes = TrialPartyEquipmentLockTypes.None_
    trial_party_accessory_master_id: Optional[int] = None
    accessory_lock_type: TrialPartyEquipmentLockTypes = (
        TrialPartyEquipmentLockTypes.None_
    )
