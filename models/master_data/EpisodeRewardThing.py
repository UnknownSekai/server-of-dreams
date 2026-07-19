from __future__ import annotations

from pydantic import BaseModel

from models.enums import ThingTypes


class EpisodeRewardThing(BaseModel):
    thing_id: int = 0
    thing_type: ThingTypes = ThingTypes.Item
    thing_quantity: int = 0
    is_only_story_event_term: bool = False
    is_chapter_all_read_reward: bool = False
