from __future__ import annotations

from pydantic import BaseModel

from models.enums import TalentBloomItemTypes


class CharacterPieceMaster(BaseModel):
    item_master_id: int = 0
    character_master_id: int = 0
    dugong_required_amount: int = 0
    talent_bloom_item_type: TalentBloomItemTypes = TalentBloomItemTypes.ActorPiece
