from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import GachaButtonTypes

if TYPE_CHECKING:
    from .GachaDetailBonusThing import GachaDetailBonusThing


class GachaDetailMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    required_ticket_m_item_id: Optional[int] = None
    required_ticket_quantity: Optional[int] = None
    free_jewel_amount: Optional[int] = None
    paid_jewel_amount: Optional[int] = None
    is_free: bool = False
    daily_roll_limit: Optional[int] = None
    overall_roll_limit: Optional[int] = None
    prize_count: int = 0
    fixed_prize_count: int = 0
    button_type: GachaButtonTypes = GachaButtonTypes.PaidJewelTenSeries
    detail_bonus_things: Optional[list[GachaDetailBonusThing]] = None
