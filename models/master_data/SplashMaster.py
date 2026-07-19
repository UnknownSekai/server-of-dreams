from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import (
    SplashAdditionalValueTypes,
    SplashTypes,
    SplashUnlockConditionTypes,
)


class SplashMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    order: int = 0
    splash_type: SplashTypes = SplashTypes.Video
    splash_value: Optional[str] = None
    start_date: str = ""
    end_date: str = ""
    additional_splash_value0: SplashAdditionalValueTypes = (
        SplashAdditionalValueTypes.None_
    )
    additional_splash_value1: SplashAdditionalValueTypes = (
        SplashAdditionalValueTypes.None_
    )
    unlock_condition: SplashUnlockConditionTypes = SplashUnlockConditionTypes.None_
    unlock_condition_value: Optional[int] = None
