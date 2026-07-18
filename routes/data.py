from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import read_request, respond
from helpers.user_data import current_user_id, user_data
from models import *

router = APIRouter(tags=["Data"])


# /api/data/master
@router.get("/api/data/master", name="Data_GetMasterData")
async def data_get_master_data(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(MasterDataManifest())


# /api/data/user
@router.get("/api/data/user", name="Data_GetUserData")
async def data_get_user_data(request: Request):
    app: YumeApp = request.app
    user_id = await current_user_id(app, request)
    return respond(await user_data(app, user_id))
