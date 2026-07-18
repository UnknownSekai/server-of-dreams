from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import raw_response, read_request, respond
from models import *

router = APIRouter(tags=["Episodes"])


# /api/Episodes/{episodeMasterId}/Read
@router.post("/api/Episodes/{episodeMasterId}/Read", name="Episodes_CompleteRead")
async def episodes_complete_read(request: Request, episodeMasterId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response([])


# /api/Episodes/{episodeMasterId}/ReadAll
@router.post("/api/Episodes/{episodeMasterId}/ReadAll", name="Episodes_CompleteReadAll")
async def episodes_complete_read_all(request: Request, episodeMasterId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response([])


# /api/Episodes/{episodeMasterId}/GetDetails
@router.post(
    "/api/Episodes/{episodeMasterId}/GetDetails", name="Episodes_GetEpisodeDetail"
)
async def episodes_get_episode_detail(request: Request, episodeMasterId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(EpisodeResult())
