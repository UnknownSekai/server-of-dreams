from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from models.enums import PageCategories


class GameHintMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    page_category: PageCategories = PageCategories.TutorialIngame
    page_count: int = 0
