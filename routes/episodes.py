from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(tags=["Episodes"])


# /api/Episodes/{episodeMasterId}/Read
@router.post("/api/Episodes/{episodeMasterId}/Read", name="Episodes_CompleteRead")
async def episodes_complete_read(request: Request, episodeMasterId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])


# /api/Episodes/{episodeMasterId}/ReadAll
@router.post("/api/Episodes/{episodeMasterId}/ReadAll", name="Episodes_CompleteReadAll")
async def episodes_complete_read_all(request: Request, episodeMasterId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])


# /api/Episodes/{episodeMasterId}/GetDetails?episodeMasterId=
@router.post(
    "/api/Episodes/{episodeMasterId}/GetDetails", name="Episodes_GetEpisodeDetail"
)
async def episodes_get_episode_detail(request: Request, episodeMasterId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    # Story-preprocess (Sirius.StoryPreprocess). NOT fully implemented: returns [] for every
    # episode, which the client reads as empty and plays without preloaded story text. Does
    # not use common response (ParseWithoutCommonResponse APIClient).
    #
    # A populated response is an EpisodeResult [title, storyType, order,
    # EpisodeDetailAssetSource]; the client downloads EpisodeDetailAssetSource and
    # deserializes it to EpisodeDetailResult[] -- the whole script (speaker/phrase/effect/
    # background/motions per line).
    #
    # EpisodeDetailAssetSource looks like "scenes/{id}_{hash}.bin?sv=2023-11-03&se=..." -- an
    # Azure blob path + SAS token, where {id}_{hash} matches manifest/BinHash.json in the
    # wds-sirius/Adv-Resource datamine. The SAS signature is server-issued so the official
    # URL can't be reproduced, but the script itself is in that repo as episode/{id}.json
    # (StoryType/Order/Title + EpisodeDetail[] map 1:1 onto EpisodeResult/EpisodeDetailResult),
    # so a full impl would vendor those, pack EpisodeDetail[] to msgpack, and serve them under
    # our own URL.
    #
    # Which episodes return [] vs a populated result is unconfirmed: 1000000/1000001 (the
    # tutorial prologue) return [] despite having real scripts in the datamine.
    return respond([])
