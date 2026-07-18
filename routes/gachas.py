from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/Gachas", tags=["Gachas"])


# /api/Gachas
@router.get("/", name="Gachas_GetAvailableGachas")
async def gachas_get_available_gachas(request: Request):
    return respond([])
