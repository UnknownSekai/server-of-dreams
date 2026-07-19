from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from models.enums import JumpTypes

if TYPE_CHECKING:
    from .FriendInvitationMissionStageMaster import FriendInvitationMissionStageMaster


class FriendInvitationMissionMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    description: Optional[str] = None
    order: int = 0
    start_date: str = ""
    end_date: str = ""
    jump_type: JumpTypes = JumpTypes.None_
    jump_target_id: Optional[int] = None
    stages: Optional[list[FriendInvitationMissionStageMaster]] = None
