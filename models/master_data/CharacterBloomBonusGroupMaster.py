from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .CharacterBloomBonusMaster import CharacterBloomBonusMaster
    from .CharacterBloomRewardMaster import CharacterBloomRewardMaster


class CharacterBloomBonusGroupMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    bloom_bonuses: Optional[list[CharacterBloomBonusMaster]] = None
    bloom_rewards: Optional[list[CharacterBloomRewardMaster]] = None
