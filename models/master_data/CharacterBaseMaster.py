from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.enums import CharacterBaseTypes


class CharacterBaseMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    name: Optional[str] = None
    description: Optional[str] = None
    school: Optional[str] = None
    grade: Optional[int] = None
    birth_month: Optional[int] = None
    birth_day: Optional[int] = None
    height: int = 0
    hobby: Optional[str] = None
    company_master_id: int = 0
    name_romanization: Optional[str] = None
    sense_name: Optional[str] = None
    sense_effect: Optional[str] = None
    character_voice: Optional[str] = None
    profile_image_asset_id: Optional[str] = None
    age: Optional[int] = None
    family_name_romanization: Optional[str] = None
    first_name_romanization: Optional[str] = None
    pronounce_family_name: Optional[str] = None
    pronounce_first_name: Optional[str] = None
    family_name: Optional[str] = None
    first_name: Optional[str] = None
    evo_sense_name: Optional[str] = None
    evo_sense_effect: Optional[str] = None
    default_costume_master_id: int = 0
    character_base_type: CharacterBaseTypes = CharacterBaseTypes.Initial
