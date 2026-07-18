from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import raw_response, read_request, respond
from models import *

router = APIRouter(tags=["Posters"])


# /api/Posters/{uPosterId}/Breakthrough/{phaseTo}
@router.post(
    "/api/Posters/{uPosterId}/Breakthrough/{phaseTo}", name="Posters_Breakthrough"
)
async def posters_breakthrough(request: Request, uPosterId: int, phaseTo: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(BooleanResult())


# /api/Posters/ChangePosterAlternativeImage
@router.post(
    "/api/Posters/ChangePosterAlternativeImage",
    name="Posters_ChangePosterAlternativeImage",
)
async def posters_change_poster_alternative_image(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "PosterAlternativeImagePayload")
    return respond(BooleanResult())


# /api/Posters/{uPosterId}/LevelUp/{levelTo}
@router.post("/api/Posters/{uPosterId}/LevelUp/{levelTo}", name="Posters_LevelUp")
async def posters_level_up(request: Request, uPosterId: int, levelTo: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(BooleanResult())


# /api/Posters/SetFavorite
@router.post("/api/Posters/SetFavorite", name="Posters_SetPosterFavorite")
async def posters_set_poster_favorite(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "PosterFavoritePayload")
    return respond(BooleanResult())


# /api/Posters/{uPosterId}/UpdateReleasedPosterStory/{posterEpisodeType}
@router.post(
    "/api/Posters/{uPosterId}/UpdateReleasedPosterStory/{posterEpisodeType}",
    name="Posters_UpdateReleasedPosterStory",
)
async def posters_update_released_poster_story(
    request: Request, uPosterId: int, posterEpisodeType: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(BooleanResult())
