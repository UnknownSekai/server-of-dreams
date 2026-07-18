from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/data", tags=["data"])


# /api/data/master
@router.get("/master", name="Data_GetMasterData")
async def data_get_master_data(request: Request):
    return respond(MasterDataManifest())


# /api/data/user
@router.get("/user", name="Data_GetUserData")
async def data_get_user_data(request: Request):
    return respond([])
