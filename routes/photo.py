from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import raw_response, read_request, respond
from models import *

router = APIRouter(tags=["Photo"])


# /api/Photo/AbilityVarietyUp
@router.post("/api/Photo/AbilityVarietyUp", name="Photo_AbilityVarietyUp")
async def photo_ability_variety_up(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "AbilityVarietyUpPayload")
    return respond(BooleanResult())


# /api/Photo/AlbumDetailArranging
@router.post("/api/Photo/AlbumDetailArranging", name="Photo_AlbumDetailArranging")
async def photo_album_detail_arranging(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "AlbumArrangingPayload")
    return respond(BooleanResult())


# /api/Photo/AlbumReset?isAllReset=
@router.post("/api/Photo/AlbumReset", name="Photo_AlbumReset")
async def photo_album_reset(request: Request, isAllReset: Optional[bool] = None):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(BooleanResult())


# /api/Photo/AlbumSimpleArranging
@router.post("/api/Photo/AlbumSimpleArranging", name="Photo_AlbumSimpleArranging")
async def photo_album_simple_arranging(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "AlbumArrangingPayload")
    return respond(BooleanResult())


# /api/Photo/ChangePhotoAbility
@router.post("/api/Photo/ChangePhotoAbility", name="Photo_ChangePhotoAbility")
async def photo_change_photo_ability(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "ChangePhotoAbilityPayload")
    return respond(BooleanResult())


# /api/Photo/Preset/Change/{presetOrder}
@router.post("/api/Photo/Preset/Change/{presetOrder}", name="Photo_ChangePreset")
async def photo_change_preset(request: Request, presetOrder: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(BooleanResult())


# /api/Photos/FinishGeneratePhoto
@router.post("/api/Photos/FinishGeneratePhoto", name="Photo_FinishGeneratePhoto")
async def photo_finish_generate_photo(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Photos/GeneratePhoto
@router.post("/api/Photos/GeneratePhoto", name="Photo_GeneratePhoto")
async def photo_generate_photo(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "GeneratePhotoPayload")
    return respond(GeneratePhotoResult())


# /api/Photos/GeneratePhotos
@router.post("/api/Photos/GeneratePhotos", name="Photo_GeneratePhotos")
async def photo_generate_photos(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "GeneratePhotosPayload")
    return respond([])


# /api/Photo/GetAlbumMainPage?targetUserId=
@router.post("/api/Photo/GetAlbumMainPage", name="Photo_GetAlbumMainPage")
async def photo_get_album_main_page(
    request: Request, targetUserId: Optional[str] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(AlbumPageSearchResult())


# /api/Photo/IncreaseAcquirablePhotoLimit?toPhase=
@router.post(
    "/api/Photo/IncreaseAcquirablePhotoLimit", name="Photo_IncreaseAcquirablePhotoLimit"
)
async def photo_increase_acquirable_photo_limit(
    request: Request, toPhase: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(BooleanResult())


# /api/Photos/PhotoLevelUp
@router.post("/api/Photos/PhotoLevelUp", name="Photo_PhotoLevelUp")
async def photo_photo_level_up(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "LevelUpPhotoPayload")
    return respond(LevelUpPhotoResult())


# /api/Photos/RegeneratePhoto?uPhotoId=
@router.post("/api/Photos/RegeneratePhoto", name="Photo_RegeneratePhoto")
async def photo_regenerate_photo(request: Request, uPhotoId: Optional[int] = None):
    app: YumeApp = request.app
    payload = await read_request(request, "GeneratePhotoPayload")
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(GeneratePhotoResult())


# /api/Photos/Sell
@router.post("/api/Photos/Sell", name="Photo_Sell")
async def photo_sell(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request)
    return respond(BooleanResult())


# /api/Photo/SetAlbumPublishing
@router.post("/api/Photo/SetAlbumPublishing", name="Photo_SetAlbumPublishing")
async def photo_set_album_publishing(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "SetAlbumPublishingPayload")
    return respond(BooleanResult())


# /api/Photo/SetCharacterBaseTags
@router.post("/api/Photo/SetCharacterBaseTags", name="Photo_SetCharacterBaseTags")
async def photo_set_character_base_tags(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "SetPhotoTagPayload")
    return respond(BooleanResult())


# /api/Photo/Preset/SetName/{presetOrder}
@router.post("/api/Photo/Preset/SetName/{presetOrder}", name="Photo_SetPresetName")
async def photo_set_preset_name(request: Request, presetOrder: int):
    app: YumeApp = request.app
    payload = await read_request(request)
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(BooleanResult())


# /api/Photos/{photoId}/SwitchLock
@router.post("/api/Photos/{photoId}/SwitchLock", name="Photo_SwitchLock")
async def photo_switch_lock(request: Request, photoId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(BooleanResult())


# /api/Photo/WatchMusicVideo?mMusicVideoId=
@router.post("/api/Photo/WatchMusicVideo", name="Photo_WatchMusicVideo")
async def photo_watch_music_video(
    request: Request, mMusicVideoId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(BooleanResult())


# /api/Photo/WatchTheaterStory?mTheaterStoryId=
@router.post("/api/Photo/WatchTheaterStory", name="Photo_WatchTheaterStory")
async def photo_watch_theater_story(
    request: Request, mTheaterStoryId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(BooleanResult())
