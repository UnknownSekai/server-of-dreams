from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/Events", tags=["Events"])


# /api/Events/TrialPartyEvent/EditParty
@router.post("/TrialPartyEvent/EditParty", name="Events_EditTrialPartyEventParty")
async def events_edit_trial_party_event_party(request: Request):
    payload = await read_request(request, "EditTrialPartyEventStagePartyPayload")
    return respond(BooleanResult())
