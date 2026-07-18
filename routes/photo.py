from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/Photo", tags=["Photo"])


# /api/Photo/AbilityVarietyUp
@router.post("/AbilityVarietyUp", name="Photo_AbilityVarietyUp")
async def photo_ability_variety_up(request: Request):
    payload = await read_request(request, "AbilityVarietyUpPayload")
    return respond(BooleanResult())


# /api/Photo/AlbumDetailArranging
@router.post("/AlbumDetailArranging", name="Photo_AlbumDetailArranging")
async def photo_album_detail_arranging(request: Request):
    payload = await read_request(request, "AlbumArrangingPayload")
    return respond(BooleanResult())


# /api/Photo/AlbumSimpleArranging
@router.post("/AlbumSimpleArranging", name="Photo_AlbumSimpleArranging")
async def photo_album_simple_arranging(request: Request):
    payload = await read_request(request, "AlbumArrangingPayload")
    return respond(BooleanResult())


# /api/Photo/ChangePhotoAbility
@router.post("/ChangePhotoAbility", name="Photo_ChangePhotoAbility")
async def photo_change_photo_ability(request: Request):
    payload = await read_request(request, "ChangePhotoAbilityPayload")
    return respond(BooleanResult())


# /api/Photo/GetAlbumMainPage?targetUserId=
@router.post("/GetAlbumMainPage", name="Photo_GetAlbumMainPage")
async def photo_get_album_main_page(request: Request):
    return respond(AlbumPageSearchResult())


# /api/Photo/SetAlbumPublishing
@router.post("/SetAlbumPublishing", name="Photo_SetAlbumPublishing")
async def photo_set_album_publishing(request: Request):
    payload = await read_request(request, "SetAlbumPublishingPayload")
    return respond(BooleanResult())


# /api/Photo/SetCharacterBaseTags
@router.post("/SetCharacterBaseTags", name="Photo_SetCharacterBaseTags")
async def photo_set_character_base_tags(request: Request):
    payload = await read_request(request, "SetPhotoTagPayload")
    return respond(BooleanResult())
