from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import CustomLayoutActionTypes, CustomLayoutUITypes, JumpTypes


class SpecialEventLayout(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    ui_type: CustomLayoutUITypes = CustomLayoutUITypes.None_
    ui_value: Optional[str] = None
    anchor_x_percent: int = 0
    anchor_y_percent: int = 0
    position_x: float = 0.0
    position_y: float = 0.0
    size_x: float = 0.0
    size_y: float = 0.0
    scale_x: float = 0.0
    scale_y: float = 0.0
    layer: int = 0
    action_type: CustomLayoutActionTypes = CustomLayoutActionTypes.None_
    action_value: Optional[str] = None
    jump_type: JumpTypes = JumpTypes.None_
    jump_value: Optional[str] = None
    start_date: str = ""
    end_date: str = ""
