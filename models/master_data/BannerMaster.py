from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import BannerDeleteConditionTypes, JumpTypes, WebLinkTypes


class BannerMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    order: int = 0
    name: Optional[str] = None
    jump_type: JumpTypes = JumpTypes.None_
    jump_page_id: Optional[str] = None
    web_link_type: Optional[WebLinkTypes] = None
    link_url: Optional[str] = None
    delete_condition_type: BannerDeleteConditionTypes = (
        BannerDeleteConditionTypes.BuyItem
    )
    delete_condition_value: Optional[str] = None
    image_path: Optional[str] = None
    start_date: str = ""
    end_date: str = ""
