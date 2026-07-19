from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import (
    PossessionRarities,
    PosterOrientation,
    PosterSubTitleDisplayConditions,
)

if TYPE_CHECKING:
    from .PosterCostumeMaster import PosterCostumeMaster


class PosterMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name: Optional[str] = None
    organize_restrict_group_id: Optional[int] = None
    rarity: PossessionRarities = PossessionRarities.R
    level_pattern_group_master_id: int = 0
    sub_title_position_x1: Optional[float] = None
    sub_title_position_y1: Optional[float] = None
    sub_title_position_x2: Optional[float] = None
    sub_title_position_y2: Optional[float] = None
    sub_title_position_x3: Optional[float] = None
    sub_title_position_y3: Optional[float] = None
    release_item_group_id: int = 0
    pronounce_name: Optional[str] = None
    costumes: Optional[list[PosterCostumeMaster]] = None
    appearance_character_base_master_ids: Optional[list[int]] = None
    is_restrict_item_break_through: bool = False
    display_start_at: str = ""
    display_end_at: str = ""
    unlock_text: Optional[str] = None
    orientation: PosterOrientation = PosterOrientation.Portrait
    sub_title_display_condition: PosterSubTitleDisplayConditions = (
        PosterSubTitleDisplayConditions.None_
    )
    sub_title_display_condition_value: Optional[int] = None
    poster_breakthrough_max_phase: Optional[int] = None
    poster_breakthrough_max_phase_release_date: Optional[str] = None
    secondary_sub_title_display_condition: PosterSubTitleDisplayConditions = (
        PosterSubTitleDisplayConditions.None_
    )
    secondary_sub_title_display_condition_value: Optional[int] = None
    alternate_image_position_x1: Optional[float] = None
    alternate_image_position_y1: Optional[float] = None
    alternate_image_release_phase1: Optional[int] = None
    alternate_image_position_x2: Optional[float] = None
    alternate_image_position_y2: Optional[float] = None
    alternate_image_release_phase2: Optional[int] = None
    alternate_image_position_x3: Optional[float] = None
    alternate_image_position_y3: Optional[float] = None
    alternate_image_release_phase3: Optional[int] = None
