import io
import time
import uuid
from pathlib import Path
from typing import Optional

import msgpack
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse

from core import YumeApp
from helpers import game_state as gs
from helpers.cache import cache
from helpers.msgpack import _decompress, fault, read_request, respond
from models import *

router = APIRouter(tags=["Photo"])

PHOTO_ROOT = Path(__file__).resolve().parent.parent / "_data" / "photos"


async def _watch(
    request: Request, entity: str, field: str, ident: int, valid
) -> object:
    try:
        if not ident or not valid:
            raise gs.Rejected()
        async with gs.transaction(request) as s:
            row = await s.one(entity, **{field: ident})
            if row:
                await s.update(entity, row, **{field: ident})
            else:
                await s.insert(entity, **{field: ident})
        return respond(BooleanResult(is_success=True), present=s.present())
    except gs.Rejected:
        return respond(BooleanResult())


# /api/Photo/WatchMusicVideo?mMusicVideoId=
@router.post("/api/Photo/WatchMusicVideo", name="Photo_WatchMusicVideo")
async def photo_watch_music_video(request: Request, mMusicVideoId: int = 0):
    return await _watch(
        request,
        "MusicVideo",
        "musicVideoMasterId",
        mMusicVideoId,
        gs.master("music_video_master", mMusicVideoId),
    )


# /api/Photo/WatchTheaterStory?mTheaterStoryId=
@router.post("/api/Photo/WatchTheaterStory", name="Photo_WatchTheaterStory")
async def photo_watch_theater_story(request: Request, mTheaterStoryId: int = 0):
    valid = any(
        story.id_ == mTheaterStoryId
        for chapter in cache.theater_chapter_master
        for story in chapter.stories or []
    )
    return await _watch(
        request, "TheaterStory", "theaterStoryMasterId", mTheaterStoryId, valid
    )


def _film_rarity(film: int) -> int:
    # Exact server lottery weights were never exposed; preserve the documented minimum tier.
    if film not in range(510001, 510007):
        raise gs.Rejected("Unsupported film")
    return min(film - 510000, 5)


def _jpeg(data) -> bytes:
    if (
        not isinstance(data, bytes)
        or not 4 <= len(data) <= 12_000_000
        or not data.startswith(b"\xff\xd8")
    ):
        raise gs.Rejected("Invalid photo image")
    from PIL import Image

    try:
        with Image.open(io.BytesIO(data)) as im:
            if im.format != "JPEG" or im.width * im.height > 40_000_000:
                raise gs.Rejected("Invalid dimensions")
            im.verify()
    except (OSError, ValueError) as e:
        raise gs.Rejected("Invalid JPEG") from e
    return data


# /photo/{variant}/{filename}  (local photo image serving)
@router.get("/photo/{variant}/{filename}", name="Photo_Image")
async def photo_image(variant: str, filename: str):
    if variant not in ("original", "thumbnail") or not filename.endswith(".jpg"):
        raise HTTPException(404)
    try:
        uuid.UUID(filename[:-4])
    except ValueError:
        raise HTTPException(404)
    path = PHOTO_ROOT / variant / filename
    if not path.is_file():
        raise HTTPException(404)
    return FileResponse(path, media_type="image/jpeg")


# /api/Photos/GeneratePhoto
@router.post("/api/Photos/GeneratePhoto", name="Photo_GeneratePhoto")
async def photo_generate_photo(request: Request):
    saved: list = []
    try:
        p = await read_request(request)
        if not isinstance(p, list) or len(p) != 5 or p[0] is not None:
            raise gs.Rejected("Unsupported photo request")
        rarity = _film_rarity(p[1])
        original, thumbnail = _jpeg(p[2]), _jpeg(p[3])
        if not isinstance(p[4], list) or len(p[4]) > 30:
            raise gs.Rejected("Invalid characters")
        chars = list(
            dict.fromkeys(c[0] for c in p[4] if isinstance(c, list) and len(c) == 2)
        )
        if len(chars) != len(p[4]) or any(
            not gs.master("character_base_master", c) for c in chars
        ):
            raise gs.Rejected("Invalid character")
        name = str(uuid.uuid4()) + ".jpg"
        async with gs.transaction(request) as s:
            await s.pay({p[1]: 1})
            for variant, data in [("original", original), ("thumbnail", thumbnail)]:
                path = PHOTO_ROOT / variant / name
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open("xb") as f:
                    f.write(data)
                saved.append(path)
            row = await s.insert(
                "Photo",
                fileName=name,
                sasToken="",
                photoEffectMasterId=None,
                lock=False,
                useAlbumPage=None,
                level=1,
                rarity=rarity,
                signMasterId=None,
                generatedAt=time.time_ns() // 1000,
                thumbnailSasToken="",
                appearedCharacterBaseMasterIds=chars,
                taggedCharacterBaseMasterIds=chars,
                useDecoPage=0,
            )
            for ident in (200300, 10):
                await gs.mission_progress(s, ident, create=True)
            for c in chars:
                await gs.character_progress(s, c, 9, 1)
        return respond(
            GeneratePhotoResult(
                photo_id=row["id"], file_name=name, sas_token="", rarity=rarity
            ),
            present=s.present(),
        )
    except gs.Rejected as e:
        for path in saved:
            path.unlink(missing_ok=True)
        return respond(GeneratePhotoResult(), faults=[fault("InvalidPhoto", str(e))])
    except BaseException:
        for path in saved:
            path.unlink(missing_ok=True)
        raise


# /api/Photos/FinishGeneratePhoto
@router.post("/api/Photos/FinishGeneratePhoto", name="Photo_FinishGeneratePhoto")
async def photo_finish_generate_photo(request: Request):
    async with gs.transaction(request):
        pass
    return respond(BooleanResult(is_success=True))


def _unpack_items(raw) -> list:
    try:
        value = _decompress(
            msgpack.unpackb(bytes(raw), raw=False, strict_map_key=False)
        )
        if (
            not isinstance(value, list)
            or len(value) != 1
            or not isinstance(value[0], list)
            or len(value[0]) > 200
        ):
            raise ValueError()
        return value[0]
    except (ValueError, TypeError, msgpack.UnpackException) as e:
        raise gs.Rejected("Invalid album layout") from e


# /api/Photo/AlbumSimpleArranging  &  /api/Photo/AlbumDetailArranging
@router.post("/api/Photo/AlbumSimpleArranging", name="Photo_AlbumSimpleArranging")
@router.post("/api/Photo/AlbumDetailArranging", name="Photo_AlbumDetailArranging")
async def photo_album_arranging(request: Request):
    try:
        p = await read_request(request)
        if not isinstance(p, list) or len(p) != 4:
            raise gs.Rejected("Invalid album")
        publishing, page, raw, theme = p
        if not isinstance(page, int) or page not in list(range(1, 11)) + list(
            range(101, 111)
        ):
            raise gs.Rejected("Invalid album page")
        detailed = request.url.path.endswith("DetailArranging")
        items = _unpack_items(raw)
        async with gs.transaction(request) as s:
            selected: list = []
            for item in items:
                if not isinstance(item, list) or len(item) != (12 if detailed else 5):
                    raise gs.Rejected("Invalid album item")
                kind = item[1] if detailed else 1
                if kind == 1:
                    photo = await s.one("Photo", id=item[0])
                    if not photo:
                        raise gs.Rejected("Photo is not owned")
                    if photo["id"] in selected:
                        raise gs.Rejected("Duplicate photo")
                    selected.append(photo["id"])
                    offset = 2 if detailed else 1
                    item[offset : offset + 2] = [photo["fileName"], photo["sasToken"]]
                elif kind == 3:
                    if not gs.master("album_theme_master", item[0]):
                        raise gs.Rejected("Unknown theme")
                elif kind == 2:
                    decoration = gs.master("decoration_master", item[0])
                    if not decoration or (
                        not decoration.is_default
                        and not await s.one("Decoration", decorationMasterId=item[0])
                    ):
                        raise gs.Rejected("Decoration is not owned")
                elif kind == 4:
                    stamp = gs.master("stamp_master", item[0])
                    owned = {
                        ident
                        for row in await s.rows("Stamp")
                        for ident in (row["stampMasterIds"] or [])
                    }
                    if not stamp or (not stamp.is_default and item[0] not in owned):
                        raise gs.Rejected("Stamp is not owned")
                else:
                    raise gs.Rejected("Unknown album item type")
            if theme is not None and not gs.master("album_theme_master", theme):
                raise gs.Rejected("Unknown theme")
            if detailed:
                items.sort(key=lambda x: x[1])
            normal = page < 100
            mask = 0 if normal else 1 << (page - 101)
            for photo in await s.rows("Photo"):
                if normal:
                    if photo["id"] in selected:
                        if photo["useAlbumPage"] not in (None, 0, page):
                            raise gs.Rejected("Photo is already in another album page")
                        await s.update("Photo", photo, useAlbumPage=page)
                    elif photo["useAlbumPage"] == page:
                        await s.update("Photo", photo, useAlbumPage=None)
                else:
                    flags = (
                        photo["useDecoPage"] | mask
                        if photo["id"] in selected
                        else photo["useDecoPage"] & ~mask
                    )
                    if flags != photo["useDecoPage"]:
                        await s.update("Photo", photo, useDecoPage=flags)
            values = dict(
                page=page,
                editType=2 if detailed else 1,
                publishing=bool(publishing and normal),
                items=list(msgpack.packb([items], use_bin_type=True)),
                albumThemeMasterId=None if detailed else theme,
            )
            row = await s.one("AlbumPage", page=page)
            if row:
                await s.update("AlbumPage", row, **values)
            else:
                await s.insert("AlbumPage", **values)
            album = await s.one("Album")
            if not album:
                album = await s.insert(
                    "Album", level=1, publishPageNumber=1, currentPresetOrder=1
                )
            if selected and album["level"] == 0:
                await s.update("Album", album, level=1)
            if publishing and normal:
                await s.update("Album", album, publishPageNumber=page)
                for other in await s.rows("AlbumPage"):
                    if other["page"] != page and other["publishing"]:
                        await s.update("AlbumPage", other, publishing=False)
            await gs.mission_progress(s, 11, 1 if selected else 0, create=True)
        return respond(BooleanResult(is_success=True), present=s.present())
    except gs.Rejected as e:
        return respond(BooleanResult(), faults=[fault("InvalidAlbum", str(e))])


# /api/Photo/SetCharacterBaseTags
@router.post("/api/Photo/SetCharacterBaseTags", name="Photo_SetCharacterBaseTags")
async def photo_set_character_base_tags(request: Request):
    try:
        p = await read_request(request)
        if (
            not isinstance(p, list)
            or len(p) != 2
            or not isinstance(p[1], list)
            or len(p[1]) > 100
        ):
            raise gs.Rejected()
        if any(not gs.master("character_base_master", c) for c in p[1]):
            raise gs.Rejected()
        async with gs.transaction(request) as s:
            row = await s.one("Photo", id=p[0])
            if not row:
                raise gs.Rejected()
            await s.update(
                "Photo", row, taggedCharacterBaseMasterIds=list(dict.fromkeys(p[1]))
            )
        return respond(BooleanResult(is_success=True), present=s.present())
    except gs.Rejected:
        return respond(BooleanResult())


# /api/Photo/GetAlbumMainPage?targetUserId=
@router.post("/api/Photo/GetAlbumMainPage", name="Photo_GetAlbumMainPage")
async def photo_get_album_main_page(
    request: Request, targetUserId: Optional[str] = None
):
    async with gs.transaction(request) as s:
        if targetUserId and targetUserId != str(s.uid):
            return respond([None, False])
        album = await s.one("Album")
        page = (
            await s.one("AlbumPage", page=album["publishPageNumber"]) if album else None
        )
        if not page:
            return respond([None, False])
        return respond(
            [
                [
                    page["id"],
                    album["id"],
                    album["level"],
                    page["page"],
                    page["editType"],
                    page["publishing"],
                    bytes(page["items"] or []),
                    page["albumThemeMasterId"],
                ],
                True,
            ]
        )


# ---- remaining photo endpoints (not yet implemented) ----


# /api/Photo/AbilityVarietyUp
@router.post("/api/Photo/AbilityVarietyUp", name="Photo_AbilityVarietyUp")
async def photo_ability_variety_up(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, AbilityVarietyUpPayload)
    return respond(BooleanResult())


# /api/Photo/AlbumReset?isAllReset=
@router.post("/api/Photo/AlbumReset", name="Photo_AlbumReset")
async def photo_album_reset(request: Request, isAllReset: Optional[bool] = None):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Photo/ChangePhotoAbility
@router.post("/api/Photo/ChangePhotoAbility", name="Photo_ChangePhotoAbility")
async def photo_change_photo_ability(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, ChangePhotoAbilityPayload)
    return respond(BooleanResult())


# /api/Photo/Preset/Change/{presetOrder}
@router.post("/api/Photo/Preset/Change/{presetOrder}", name="Photo_ChangePreset")
async def photo_change_preset(request: Request, presetOrder: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Photos/GeneratePhotos
@router.post("/api/Photos/GeneratePhotos", name="Photo_GeneratePhotos")
async def photo_generate_photos(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, GeneratePhotosPayload)
    return respond([GeneratePhotoResult()])


# /api/Photo/IncreaseAcquirablePhotoLimit?toPhase=
@router.post(
    "/api/Photo/IncreaseAcquirablePhotoLimit", name="Photo_IncreaseAcquirablePhotoLimit"
)
async def photo_increase_acquirable_photo_limit(
    request: Request, toPhase: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Photos/PhotoLevelUp
@router.post("/api/Photos/PhotoLevelUp", name="Photo_PhotoLevelUp")
async def photo_photo_level_up(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, LevelUpPhotoPayload)
    return respond(LevelUpPhotoResult())


# /api/Photos/RegeneratePhoto?uPhotoId=
@router.post("/api/Photos/RegeneratePhoto", name="Photo_RegeneratePhoto")
async def photo_regenerate_photo(request: Request, uPhotoId: Optional[int] = None):
    app: YumeApp = request.app
    payload = await read_request(request, GeneratePhotoPayload)
    return respond(GeneratePhotoResult())


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
    payload = await read_request(request, SetAlbumPublishingPayload)
    return respond(BooleanResult())


# /api/Photo/Preset/SetName/{presetOrder}
@router.post("/api/Photo/Preset/SetName/{presetOrder}", name="Photo_SetPresetName")
async def photo_set_preset_name(request: Request, presetOrder: int):
    app: YumeApp = request.app
    payload = await read_request(request)
    return respond(BooleanResult())


# /api/Photos/{photoId}/SwitchLock
@router.post("/api/Photos/{photoId}/SwitchLock", name="Photo_SwitchLock")
async def photo_switch_lock(request: Request, photoId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())
