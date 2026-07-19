from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(tags=["Auditions"])


# /api/Auditions/{auditionId}/CopyTo/{uPartyId}
@router.post(
    "/api/Auditions/{auditionId}/CopyTo/{uPartyId}",
    name="Auditions_CopyAuditionClearParty",
)
async def auditions_copy_audition_clear_party(
    request: Request, auditionId: int, uPartyId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Auditions/{auditionId}/HighScoreParty
@router.get(
    "/api/Auditions/{auditionId}/HighScoreParty",
    name="Auditions_GetAuditionHighScoreParty",
)
async def auditions_get_audition_high_score_party(request: Request, auditionId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(AuditionClearParty())


# /api/Auditions/{auditionId}
@router.get("/api/Auditions/{auditionId}", name="Auditions_GetAuditionInformation")
async def auditions_get_audition_information(request: Request, auditionId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(AuditionClearedInformationResult())
