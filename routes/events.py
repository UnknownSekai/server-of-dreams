from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/Events", tags=["Events"])


# /api/Events/TrialPartyEvent/EditParty
@router.post(
    "/TrialPartyEvent/EditParty",
    response_model=BooleanResult,
    name="Events_EditTrialPartyEventParty",
)
async def events_edit_trial_party_event_party(
    body: EditTrialPartyEventStagePartyPayload,
) -> BooleanResult:
    return BooleanResult()
