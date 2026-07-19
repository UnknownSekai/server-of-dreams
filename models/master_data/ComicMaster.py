from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .ComicEpisodeMaster import ComicEpisodeMaster


class ComicMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    group_name: Optional[str] = None
    episodes: Optional[list[ComicEpisodeMaster]] = None
