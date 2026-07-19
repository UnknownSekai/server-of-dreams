from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import Attributes, CharacterRarities

if TYPE_CHECKING:
    from .CharacterCategoryMaster import CharacterCategoryMaster
    from .Status import Status


class CharacterMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    character_base_master_id: int = 0
    name: Optional[str] = None
    description: Optional[str] = None
    asset_id: Optional[str] = None
    rarity: CharacterRarities = CharacterRarities.Rare1
    attribute: Attributes = Attributes.Cute
    min_level_status: Optional[Status] = None
    star_act_master_id: int = 0
    awaken_star_act_master_id: Optional[int] = None
    sense_master_id: int = 0
    forbid_generic_item_bloom: bool = False
    bloom_bonus_group_master_id: int = 0
    sense_enhance_item_group_master_id: int = 0
    first_episode_release_item_group_id: int = 0
    second_episode_release_item_group_id: int = 0
    character_awakening_item_group_master_id: Optional[int] = None
    display_start_at: str = ""
    display_end_at: str = ""
    unlock_text: Optional[str] = None
    categories: Optional[list[CharacterCategoryMaster]] = None
    leader_sense_master_id: Optional[int] = None
    max_talent_stage: int = 0
    max_talent_stage_release_date: Optional[str] = None
    secondary_character_base_master_id: Optional[int] = None
    secondary_sense_master_id: Optional[int] = None
    secondary_attribute: Optional[Attributes] = None
