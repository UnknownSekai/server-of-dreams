from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import MusicCourseType, MusicCourseUnlockConditionTypes

if TYPE_CHECKING:
    from .MusicCourseDetailMaster import MusicCourseDetailMaster


class MusicCourseMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name: Optional[str] = None
    music_course_type: MusicCourseType = MusicCourseType.DanClass
    order: int = 0
    initial_life: int = 0
    required_item_master_id: Optional[int] = None
    required_amount: int = 0
    start_date: str = ""
    end_date: Optional[str] = None
    unlock_condition: MusicCourseUnlockConditionTypes = (
        MusicCourseUnlockConditionTypes.None_
    )
    unlock_condition_value: Optional[int] = None
    tournament_qualifying_master_id: Optional[int] = None
    details: Optional[list[MusicCourseDetailMaster]] = None
