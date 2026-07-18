from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/Photos", tags=["Photos"])


# /api/Photos/FinishGeneratePhoto
@router.post("/FinishGeneratePhoto", name="Photo_FinishGeneratePhoto")
async def photo_finish_generate_photo(request: Request):
    return respond(BooleanResult())


# /api/Photos/GeneratePhoto
@router.post("/GeneratePhoto", name="Photo_GeneratePhoto")
async def photo_generate_photo(request: Request):
    payload = await read_request(request, "GeneratePhotoPayload")
    return respond(GeneratePhotoResult())


# /api/Photos/GeneratePhotos
@router.post("/GeneratePhotos", name="Photo_GeneratePhotos")
async def photo_generate_photos(request: Request):
    payload = await read_request(request, "GeneratePhotosPayload")
    return respond([])


# /api/Photos/PhotoLevelUp
@router.post("/PhotoLevelUp", name="Photo_PhotoLevelUp")
async def photo_photo_level_up(request: Request):
    payload = await read_request(request, "LevelUpPhotoPayload")
    return respond(LevelUpPhotoResult())


# /api/Photos/Sell
@router.post("/Sell", name="Photo_Sell")
async def photo_sell(request: Request):
    payload = await read_request(request, None)
    return respond(BooleanResult())
