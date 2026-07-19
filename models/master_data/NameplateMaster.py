from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import NamePlateChangeTypes

if TYPE_CHECKING:
    from .NameplateDetailMaster import NameplateDetailMaster


class NameplateMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name: Optional[str] = None
    description: Optional[str] = None
    order: int = 0
    hidden: bool = False
    is_default: bool = False
    details: Optional[list[NameplateDetailMaster]] = None
    unlock_text: Optional[str] = None
    change_type: NamePlateChangeTypes = NamePlateChangeTypes.None_
    change_value1: Optional[int] = None
    change_value2: Optional[int] = None
