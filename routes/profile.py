from fastapi import APIRouter, Request

from helpers.game_state import Rejected, mission_progress, transaction
from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(tags=["Profile"])


def _camel(name: str) -> str:
    parts = name.split("_")
    return parts[0] + "".join(p.title() for p in parts[1:])


# /api/Profiles/Edit
@router.post("/api/Profiles/Edit", name="Profile_Edit")
async def profile_edit(request: Request):
    try:
        p = await read_request(request, EditUserProfilePayload)
        if p is None:
            raise Rejected()
        values = {_camel(k): v for k, v in p.model_dump().items()}
        values["nameBaseColorMasterId"] = values.pop("nameBaseColorMasterid")
        async with transaction(request) as s:
            row = await s.one("UserProfile")
            if not row:
                raise Rejected()
            actor = (
                await s.one("Character", id=p.main_u_character_id)
                if p.main_u_character_id
                else await s.one(
                    "Character", characterMasterId=p.main_character_master_id
                )
            )
            if not actor or actor["characterMasterId"] != p.main_character_master_id:
                raise Rejected()
            if p.name is not None and len(p.name) > 100:
                raise Rejected()
            if p.introduction is not None and len(p.introduction) > 1000:
                raise Rejected()
            if values["introduction"] != row["introduction"]:
                await mission_progress(s, 28, create=True)
            if any(
                values[k] != row[k] for k in ("mTrophyId1", "mTrophyId2", "mTrophyId3")
            ):
                await mission_progress(s, 27, create=True)
            await s.update("UserProfile", row, **values)
        return respond(BooleanResult(is_success=True), present=s.present())
    except Rejected:
        return respond(BooleanResult())
