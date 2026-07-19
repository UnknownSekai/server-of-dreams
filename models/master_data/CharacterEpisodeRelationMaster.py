from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class CharacterEpisodeRelationMaster(BaseModel):
    character_masterid: int = 0
    previous_story_master_ids: Optional[list[int]] = None
    next_story_master_ids: Optional[list[int]] = None
    side_story_character_master_ids: Optional[list[int]] = None
    related_story_master_ids: Optional[list[int]] = None
