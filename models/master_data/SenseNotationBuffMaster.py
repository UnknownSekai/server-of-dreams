from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import SenseNotationBuffTypes, SenseNotationStatusTypes


class SenseNotationBuffMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    type: SenseNotationBuffTypes = SenseNotationBuffTypes.None_
    target_value: Optional[int] = None
    buff_value: int = 0
    status_type: SenseNotationStatusTypes = SenseNotationStatusTypes.Performance
