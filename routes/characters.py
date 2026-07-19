from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(tags=["Characters"])


# /api/Characters/{characterId}/AddExperience
@router.post(
    "/api/Characters/{characterId}/AddExperience", name="Characters_AddExperience"
)
async def characters_add_experience(request: Request, characterId: int):
    app: YumeApp = request.app
    payload = await read_request(request, UseExperienceItemsPayload)
    return respond(BooleanResult())


# /api/Characters/{characterId}/Awaken
@router.post("/api/Characters/{characterId}/Awaken", name="Characters_Awaken")
async def characters_awaken(request: Request, characterId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Characters/{characterId}/BloomTalent/{stageTo}
@router.post(
    "/api/Characters/{characterId}/BloomTalent/{stageTo}", name="Characters_BloomTalent"
)
async def characters_bloom_talent(request: Request, characterId: int, stageTo: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Characters/BulkLevelUp
@router.post("/api/Characters/BulkLevelUp", name="Characters_BulkLevelUp")
async def characters_bulk_level_up(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, BulkLevelUpPayload)
    return respond(BooleanResult())


# /api/Characters/{characterId}/EnhanceSenseLevel/{levelTo}?priority=
@router.post(
    "/api/Characters/{characterId}/EnhanceSenseLevel/{levelTo}",
    name="Characters_EnhanceSenseLevel",
)
async def characters_enhance_sense_level(
    request: Request, characterId: int, levelTo: int, priority: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Characters/LinkCharacter?mCharacterBaseId=&linkedMCharacterBaseId=
@router.post("/api/Characters/LinkCharacter", name="Characters_LinkCharacter")
async def characters_link_character(
    request: Request,
    mCharacterBaseId: Optional[int] = None,
    linkedMCharacterBaseId: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])


# /api/Characters/ReceiveLinkCharacterReward?mCharacterBaseId=
@router.post(
    "/api/Characters/ReceiveLinkCharacterReward",
    name="Characters_ReceiveLinkCharacterReward",
)
async def characters_receive_link_character_reward(
    request: Request, mCharacterBaseId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])


# /api/Characters/{characterMasterId}/ReleaseSideStory?order=
@router.post(
    "/api/Characters/{characterMasterId}/ReleaseSideStory",
    name="Characters_ReleaseSideStory",
)
async def characters_release_side_story(
    request: Request, characterMasterId: int, order: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Characters/SetFavorite
@router.post("/api/Characters/SetFavorite", name="Characters_SetCharacterFavorite")
async def characters_set_character_favorite(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, CharacterFavoritePayload)
    return respond(BooleanResult())


# /api/CharacterBases/{characterBaseMasterId}/SetCostume/{costumeMasterId}
@router.post(
    "/api/CharacterBases/{characterBaseMasterId}/SetCostume/{costumeMasterId}",
    name="Characters_SetCostume",
)
async def characters_set_costume(
    request: Request, characterBaseMasterId: int, costumeMasterId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Characters/Portal/SetCharacter
@router.post(
    "/api/Characters/Portal/SetCharacter", name="Characters_SetPortalMCharacter"
)
async def characters_set_portal_mcharacter(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, ActorPortalCharacterPayload)
    return respond(BooleanResult())


# /api/Characters/{characterId}/SwitchCharacterDisplayAwakeningStatusAsync
@router.post(
    "/api/Characters/{characterId}/SwitchCharacterDisplayAwakeningStatusAsync",
    name="Characters_SwitchCharacterDisplayAwakeningStatus",
)
async def characters_switch_character_display_awakening_status(
    request: Request, characterId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Characters/UpdateSelectionType?characterId=&selectionType=
@router.post(
    "/api/Characters/UpdateSelectionType", name="Characters_UpdateSelectionType"
)
async def characters_update_selection_type(
    request: Request,
    characterId: Optional[int] = None,
    selectionType: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())
