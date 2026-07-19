from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import PhotoRarities

if TYPE_CHECKING:
    from .PhotoLevelUpItemMaster import PhotoLevelUpItemMaster


class PhotoLevelUpItemGroupMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    rarity: PhotoRarities = PhotoRarities.Rare1
    base_level: int = 0
    required_coin: int = 0
    items: Optional[list[PhotoLevelUpItemMaster]] = None
