from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class FacialExpressionMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    eye_brow: Optional[str] = None
    eye: Optional[str] = None
    eye_blink: Optional[str] = None
    cheek: Optional[str] = None
    mouth: Optional[str] = None
