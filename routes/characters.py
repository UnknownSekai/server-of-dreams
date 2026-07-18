from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/Characters", tags=["Characters"])


# /api/Characters/BulkLevelUp
@router.post("/BulkLevelUp", name="Characters_BulkLevelUp")
async def characters_bulk_level_up(request: Request):
    payload = await read_request(request, None)
    return respond(BooleanResult())


# /api/Characters/Portal/SetCharacter
@router.post("/Portal/SetCharacter", name="Characters_SetPortalMCharacter")
async def characters_set_portal_m_character(request: Request):
    payload = await read_request(request, "ActorPortalCharacterPayload")
    return respond(BooleanResult())


# /api/Characters/SetFavorite
@router.post("/SetFavorite", name="Characters_SetCharacterFavorite")
async def characters_set_character_favorite(request: Request):
    payload = await read_request(request, "CharacterFavoritePayload")
    return respond(BooleanResult())
