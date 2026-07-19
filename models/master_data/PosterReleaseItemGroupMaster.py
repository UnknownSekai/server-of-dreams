from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .PosterReleaseItemMaster import PosterReleaseItemMaster


class PosterReleaseItemGroupMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    items: Optional[list[PosterReleaseItemMaster]] = None
    item_consume_apply_flag: bool = False
