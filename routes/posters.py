from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/Posters", tags=["Posters"])


# /api/Posters/ChangePosterAlternativeImage
@router.post(
    "/ChangePosterAlternativeImage", name="Posters_ChangePosterAlternativeImage"
)
async def posters_change_poster_alternative_image(request: Request):
    payload = await read_request(request, "PosterAlternativeImagePayload")
    return respond(BooleanResult())


# /api/Posters/SetFavorite
@router.post("/SetFavorite", name="Posters_SetPosterFavorite")
async def posters_set_poster_favorite(request: Request):
    payload = await read_request(request, "PosterFavoritePayload")
    return respond(BooleanResult())
