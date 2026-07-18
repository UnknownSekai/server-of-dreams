from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/Leagues", tags=["Leagues"])


# /api/Leagues
@router.get("/", name="Leagues_SendThingLeagueRewards")
async def leagues_send_thing_league_rewards(request: Request):
    return respond(LeagueReceiveResults())


# /api/Leagues/TopMenuInformation
@router.post("/TopMenuInformation", name="Leagues_GetTopMenuInformation")
async def leagues_get_top_menu_information(request: Request):
    return respond(LeagueTopMenuInformationResult())
