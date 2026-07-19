from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .SenseNotationBuffMaster import SenseNotationBuffMaster
    from .SenseNotationDetailMaster import SenseNotationDetailMaster


class SenseNotationMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    details: Optional[list[SenseNotationDetailMaster]] = None
    buffs: Optional[list[SenseNotationBuffMaster]] = None
