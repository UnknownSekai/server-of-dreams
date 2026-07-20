from typing import Optional

from fastapi import APIRouter, Request, Response
from starlette.exceptions import HTTPException
from core import YumeApp

from db.user import get_episodes, update_episode_read_all, upsert_episode
from helpers.episodes import (
    episode_read_reward_things,
    episode_readall_reward_things,
    episode_result,
    episode_scene_bin,
    scene_bin_name,
)
from helpers.msgpack import read_request, respond
from helpers.things import grant_things_consolidated, present_type
from helpers.user_data import build_present, current_user_id, data_object
from models import *
from models.database import EpisodeModel

router = APIRouter(tags=["Episodes"])


async def _complete_read(
    app: YumeApp, user_id: int, episode_master_id: int, read_all: bool
):
    """Read (skip) grants the read reward (the episode's package) once. ReadAll additionally
    grants the read-all reward (the 歌劇目録 catalogue item) once. Each is granted only if not
    already claimed, so read-then-readall gives the read-all reward exactly once and doesn't
    re-grant the read reward. Returns the granted ReceivedThing[] + present (Episode +
    resources). Missions are not handled yet."""
    # TODO: verify the caller has this episode unlocked (release conditions) before rewarding.
    things: list[tuple[int, int, int]] = []
    final_read_all = read_all
    async with app.acquire_db() as conn:
        episodes = await conn.fetch(get_episodes(user_id))
        existing = next(
            (e for e in episodes if e.episodeMasterId == episode_master_id), None
        )
        if existing is None:  # first read -> read reward (+ read-all reward if ReadAll)
            things = list(episode_read_reward_things(episode_master_id))
            if read_all:
                things += episode_readall_reward_things(episode_master_id)
            await conn.execute(
                upsert_episode(
                    user_id,
                    {"episodeMasterId": episode_master_id, "hasReadAll": read_all},
                )
            )
        else:
            final_read_all = existing.hasReadAll or read_all
            if read_all and not existing.hasReadAll:  # read before, now read-all
                things = list(episode_readall_reward_things(episode_master_id))
                await conn.execute(
                    update_episode_read_all(user_id, episode_master_id, True)
                )

        result = (
            await grant_things_consolidated(conn, user_id, things) if things else []
        )

    present = [
        data_object(
            "Episode",
            EpisodeModel(
                userId=user_id,
                episodeMasterId=episode_master_id,
                hasReadAll=final_read_all,
            ),
        )
    ]
    if result:
        # only the granted items belong in present, not the whole inventory (item row id ==
        # item master id, so we can scope the Item refresh to the ids we just granted).
        item_ids = {int(r.id_) for r in result if present_type(int(r.type)) == "Item"}
        specs: list = [
            t for t in {present_type(int(r.type)) for r in result} if t and t != "Item"
        ]
        if item_ids:
            specs.append(("Item", item_ids))
        present += await build_present(app, user_id, *specs)
    return respond(result, present=present)


# Scene script blob: EpisodeDetailResult[] packed to msgpack, served as the .bin the client
# downloads (from an EpisodeResult.EpisodeDetailAssetSource)
@router.get("/master-data/production/scenes/{filename}", name="Episodes_SceneBin")
async def episodes_scene_bin(request: Request, filename: str) -> Response:
    if not filename.endswith(".bin"):
        raise HTTPException(status_code=404)
    name = filename[:-4]  # "<id>_<hash>"
    try:
        episode_id = int(name.split("_", 1)[0])
    except ValueError:
        raise HTTPException(status_code=404)
    if name != scene_bin_name(episode_id):  # id + hash must match the manifest exactly
        raise HTTPException(status_code=404)
    data = episode_scene_bin(episode_id)
    if data is None:
        raise HTTPException(status_code=404)
    return Response(content=data, media_type="application/octet-stream")


# /api/Episodes/{episodeMasterId}/Read  (read by skipping -> has_read_all = false)
@router.post("/api/Episodes/{episodeMasterId}/Read", name="Episodes_CompleteRead")
async def episodes_complete_read(request: Request, episodeMasterId: int):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    if user_id is None:
        return respond([])
    return await _complete_read(app, user_id, episodeMasterId, read_all=False)


# /api/Episodes/{episodeMasterId}/ReadAll  (read all the text -> has_read_all = true)
@router.post("/api/Episodes/{episodeMasterId}/ReadAll", name="Episodes_CompleteReadAll")
async def episodes_complete_read_all(request: Request, episodeMasterId: int):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    if user_id is None:
        return respond([])
    return await _complete_read(app, user_id, episodeMasterId, read_all=True)


# /api/Episodes/{episodeMasterId}/GetDetails
@router.post(
    "/api/Episodes/{episodeMasterId}/GetDetails", name="Episodes_GetEpisodeDetail"
)
async def episodes_get_episode_detail(request: Request, episodeMasterId: int):
    app: YumeApp = request.app
    # TODO: verify the caller has this episode unlocked (release conditions) before serving it.
    # Returns a single EpisodeResult (title/storyType/order + EpisodeDetailAssetSource); the
    # client downloads that asset source to get the EpisodeDetailResult[] script. Uses the
    # common response envelope -- ParseWithoutCommonResponse just reads its `result`. An episode
    # we don't have vendored yields an empty EpisodeResult.
    result = episode_result(episodeMasterId)
    return respond(result if result is not None else EpisodeResult())
