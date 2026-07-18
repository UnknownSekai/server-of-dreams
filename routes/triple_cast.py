from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/TripleCast", tags=["TripleCast"])


# /api/TripleCast
@router.get("/", name="Leagues_SendTripleCastThingLeagueRewards")
async def leagues_send_triple_cast_thing_league_rewards(request: Request):
    return respond(LeagueReceiveResults())


# /api/TripleCast/TopMenuInformation
@router.post("/TopMenuInformation", name="Leagues_GetTripleCastTopMenuInformation")
async def leagues_get_triple_cast_top_menu_information(request: Request):
    return respond(LeagueTopMenuInformationResult())
