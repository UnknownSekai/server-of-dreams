from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import MusicCourseCertificationGrade

if TYPE_CHECKING:
    from .MusicCourseRewardThing import MusicCourseRewardThing


class MusicCourseRewardGroupMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    music_course_master_id: int = 0
    required_certification_grade: MusicCourseCertificationGrade = (
        MusicCourseCertificationGrade.None_
    )
    rewards: Optional[list[MusicCourseRewardThing]] = None
