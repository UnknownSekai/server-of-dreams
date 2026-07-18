from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import raw_response, read_request, respond
from models import *

router = APIRouter(tags=["Gachas"])


# /api/Gachas/DecideReRollGacha?gachaDetailMasterId=
@router.post("/api/Gachas/DecideReRollGacha", name="Gachas_DecideReRollGacha")
async def gachas_decide_re_roll_gacha(
    request: Request, gachaDetailMasterId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(BooleanResult())


# /api/Gachas
@router.get("/api/Gachas", name="Gachas_GetAvailableGachas")
async def gachas_get_available_gachas(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])


# /api/Gachas/CharacterLineup/{gachaMasterId}
@router.get(
    "/api/Gachas/CharacterLineup/{gachaMasterId}", name="Gachas_GetCharacterGachaLineup"
)
async def gachas_get_character_gacha_lineup(request: Request, gachaMasterId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(CharacterLineupResult())


# /api/Gachas/GetGachaHistories?cardType=
@router.post("/api/Gachas/GetGachaHistories", name="Gachas_GetGachaHistories")
async def gachas_get_gacha_histories(request: Request, cardType: Optional[int] = None):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response([])


# /api/Gachas/PosterLineup/{gachaMasterId}
@router.get(
    "/api/Gachas/PosterLineup/{gachaMasterId}", name="Gachas_GetPosterGachaLineup"
)
async def gachas_get_poster_gacha_lineup(request: Request, gachaMasterId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(PosterLineupResult())


# /api/Gachas/GetReRollGachaResults?gachaDetailMasterId=
@router.post("/api/Gachas/GetReRollGachaResults", name="Gachas_GetReRollGachaResults")
async def gachas_get_re_roll_gacha_results(
    request: Request, gachaDetailMasterId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(GachaRollResult())


# /api/Gachas/{gachaMasterId}/SelectedThings
@router.get(
    "/api/Gachas/{gachaMasterId}/SelectedThings", name="Gachas_GetSelectedThings"
)
async def gachas_get_selected_things(request: Request, gachaMasterId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(GachaSelectedThingsResult())


# /api/Gachas/ReRollGacha?gachaDetailMasterId=
@router.post("/api/Gachas/ReRollGacha", name="Gachas_ReRollGacha")
async def gachas_re_roll_gacha(
    request: Request, gachaDetailMasterId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(GachaRollResult())


# /api/Gachas/Roll/{gachaDetailMasterId}
@router.post("/api/Gachas/Roll/{gachaDetailMasterId}", name="Gachas_RollGacha")
async def gachas_roll_gacha(request: Request, gachaDetailMasterId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(GachaRollResult())


# /api/Gachas/{gachaMasterId}/SetSelectedThings
@router.post(
    "/api/Gachas/{gachaMasterId}/SetSelectedThings", name="Gachas_SetSelectedThings"
)
async def gachas_set_selected_things(request: Request, gachaMasterId: int):
    app: YumeApp = request.app
    payload = await read_request(request, "SetSelectedThingsPayload")
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(GachaSelectedThingsResult())
