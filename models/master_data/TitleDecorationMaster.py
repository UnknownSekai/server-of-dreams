from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from models.enums import TitleDecorationTypes


class TitleDecorationMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    decoration_type: TitleDecorationTypes = TitleDecorationTypes.FirstAnniversary
    start_date: str = ""
    end_date: str = ""
