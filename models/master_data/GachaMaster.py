from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import (
    GachaCardTypes,
    GachaDisplayFooterConditions,
    GachaGroupTypes,
    GachaTypes,
    GachaUnlockTypes,
)

if TYPE_CHECKING:
    from .GachaBonusThing import GachaBonusThing
    from .GachaDetailMaster import GachaDetailMaster
    from .GachaRollBonus import GachaRollBonus
    from .GachaThing import GachaThing


class GachaMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name: Optional[str] = None
    card_type: GachaCardTypes = GachaCardTypes.Character
    gacha_type: GachaTypes = GachaTypes.Pickup
    gacha_text_template_master_id: int = 0
    start_date: str = ""
    end_date: str = ""
    bonus_things: Optional[list[GachaBonusThing]] = None
    gacha_details: Optional[list[GachaDetailMaster]] = None
    things: Optional[list[GachaThing]] = None
    has_movie: bool = False
    story_event_master_id: Optional[int] = None
    attention_gacha_text_template_master_id: int = 0
    is_force_display: bool = False
    is_hide_end_date: bool = False
    unlock_type: GachaUnlockTypes = GachaUnlockTypes.None_
    unlock_value: Optional[int] = None
    exchange_shop_banner_path: Optional[str] = None
    order: int = 0
    display_footer_condition: Optional[GachaDisplayFooterConditions] = None
    group_type: GachaGroupTypes = GachaGroupTypes.None_
    roll_bonuses: Optional[list[GachaRollBonus]] = None
    re_roll_limit: Optional[int] = None
    replace_asset_name: Optional[str] = None
