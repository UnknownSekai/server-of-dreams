from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .ConcoursDetailMaster import ConcoursDetailMaster
    from .ConcoursPointMaster import ConcoursPointMaster


class ConcoursMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    event_master_id: int = 0
    bgm_path: Optional[str] = None
    details: Optional[list[ConcoursDetailMaster]] = None
    points: Optional[list[ConcoursPointMaster]] = None
