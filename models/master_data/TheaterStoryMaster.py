from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .TheaterDetailMaster import TheaterDetailMaster
    from .TheaterRoleMaster import TheaterRoleMaster


class TheaterStoryMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name: Optional[str] = None
    order: int = 0
    has_synopsis: bool = False
    synopsis: Optional[str] = None
    display_start_at: str = ""
    display_end_at: str = ""
    roles: Optional[list[TheaterRoleMaster]] = None
    details: Optional[list[TheaterDetailMaster]] = None
