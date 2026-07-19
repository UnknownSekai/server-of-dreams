from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from models.enums import CharacterProfileRestrictionItem


class CharacterProfileRestrictionMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    character_base_master_id: int = 0
    profile_restriction_item: CharacterProfileRestrictionItem = (
        CharacterProfileRestrictionItem.Birthday
    )
    unlock_condition_master_id: int = 0
    profile_unlock_value: int = 0
