from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import TitleBackgroundPriorityTypes

if TYPE_CHECKING:
    from .TitleBackgroundDetailMaster import TitleBackgroundDetailMaster


class TitleBackgroundMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    priority: TitleBackgroundPriorityTypes = TitleBackgroundPriorityTypes.Normal
    start_date: str = ""
    end_date: str = ""
    details: Optional[list[TitleBackgroundDetailMaster]] = None
