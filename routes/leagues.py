from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import raw_response, read_request, respond
from models import *

router = APIRouter(tags=["Leagues"])


# /api/Leagues/GlobalRanking/{leagueMasterId}
@router.post(
    "/api/Leagues/GlobalRanking/{leagueMasterId}", name="Leagues_GetGlobalRanking"
)
async def leagues_get_global_ranking(request: Request, leagueMasterId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response([])


# /api/Leagues/GroupRanking/{leagueMasterId}/{leagueGroupId}
@router.post(
    "/api/Leagues/GroupRanking/{leagueMasterId}/{leagueGroupId}",
    name="Leagues_GetGroupRanking",
)
async def leagues_get_group_ranking(
    request: Request, leagueMasterId: int, leagueGroupId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response([])


# /api/Leagues/TopMenuInformation
@router.post("/api/Leagues/TopMenuInformation", name="Leagues_GetTopMenuInformation")
async def leagues_get_top_menu_information(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(LeagueTopMenuInformationResult())


# /api/TripleCast/GlobalRanking/{tripleCastMasterId}
@router.post(
    "/api/TripleCast/GlobalRanking/{tripleCastMasterId}",
    name="Leagues_GetTripleCastGlobalRanking",
)
async def leagues_get_triple_cast_global_ranking(
    request: Request, tripleCastMasterId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response([])


# /api/TripleCast/GroupRanking/{tripleCastMasterId}
@router.post(
    "/api/TripleCast/GroupRanking/{tripleCastMasterId}",
    name="Leagues_GetTripleCastGroupRanking",
)
async def leagues_get_triple_cast_group_ranking(
    request: Request, tripleCastMasterId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response([])


# /api/TripleCast/TopMenuInformation
@router.post(
    "/api/TripleCast/TopMenuInformation", name="Leagues_GetTripleCastTopMenuInformation"
)
async def leagues_get_triple_cast_top_menu_information(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(LeagueTopMenuInformationResult())


# /api/Leagues
@router.get("/api/Leagues", name="Leagues_SendThingLeagueRewards")
async def leagues_send_thing_league_rewards(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(LeagueReceiveResults())


# /api/TripleCast
@router.get("/api/TripleCast", name="Leagues_SendTripleCastThingLeagueRewards")
async def leagues_send_triple_cast_thing_league_rewards(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(LeagueReceiveResults())
