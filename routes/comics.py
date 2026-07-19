from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(tags=["Comics"])


# /api/Comics/Read/{mComicEpisodeId}
@router.post("/api/Comics/Read/{mComicEpisodeId}", name="Comics_Read")
async def comics_read(request: Request, mComicEpisodeId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])
