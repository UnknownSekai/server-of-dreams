from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/Leagues", tags=["Leagues"])


# /api/Leagues
@router.get(
    "/", response_model=LeagueReceiveResults, name="Leagues_SendThingLeagueRewards"
)
async def leagues_send_thing_league_rewards() -> LeagueReceiveResults:
    return LeagueReceiveResults()


# /api/Leagues/TopMenuInformation
@router.post(
    "/TopMenuInformation",
    response_model=LeagueTopMenuInformationResult,
    name="Leagues_GetTopMenuInformation",
)
async def leagues_get_top_menu_information() -> LeagueTopMenuInformationResult:
    return LeagueTopMenuInformationResult()
