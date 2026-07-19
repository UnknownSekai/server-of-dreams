from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from models.enums import CharacterRarities, TalentBloomItemTypes


class CharacterBloomItemMaster(BaseModel):
    rarity: CharacterRarities = CharacterRarities.Rare1
    current_stage: int = 0
    required_piece_amount: int = 0
    talent_bloom_item_type: TalentBloomItemTypes = TalentBloomItemTypes.ActorPiece
    generic_bloom_item_master_id: Optional[int] = None
    required_item_master_id: Optional[int] = None
    required_item_amount: Optional[int] = None
