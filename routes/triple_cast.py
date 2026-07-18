from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/TripleCast", tags=["TripleCast"])


# /api/TripleCast
@router.get(
    "/",
    response_model=LeagueReceiveResults,
    name="Leagues_SendTripleCastThingLeagueRewards",
)
async def leagues_send_triple_cast_thing_league_rewards() -> LeagueReceiveResults:
    return LeagueReceiveResults()


# /api/TripleCast/TopMenuInformation
@router.post(
    "/TopMenuInformation",
    response_model=LeagueTopMenuInformationResult,
    name="Leagues_GetTripleCastTopMenuInformation",
)
async def leagues_get_triple_cast_top_menu_information() -> (
    LeagueTopMenuInformationResult
):
    return LeagueTopMenuInformationResult()
