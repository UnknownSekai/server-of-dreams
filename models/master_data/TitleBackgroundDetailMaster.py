from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import TitleBackgroundPathTypes


class TitleBackgroundDetailMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    path_type: TitleBackgroundPathTypes = TitleBackgroundPathTypes.Path
    path_value: Optional[str] = None
    is_title_hide: bool = False
    is_decoration_hide: bool = False
