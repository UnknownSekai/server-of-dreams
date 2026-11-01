from collections import Counter

from fastapi import APIRouter, Request

from core import YumeApp
from helpers.cache import cache
from helpers.game_state import Rejected, State, master, star_points, transaction
from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(tags=["CharacterMission"])


async def _claim_star_rewards(s: State, base_master_id: int) -> "StarPointResult":
    """Claim every pending character-mission stage reward for one base and rank it up.
    Star points from a category are split evenly across that category's stages."""
    base = await s.one("CharacterBase", characterBaseMasterId=base_master_id)
    if not base:
        raise Rejected()
    rank_before = base["starRank"]
    points_before = base["totalStarPoint"]
    points = 0
    categories = {x.id_: x for x in cache.character_mission_category_level_master}
    all_stages = [st for m in cache.character_mission_master for st in m.stages or []]
    sizes = Counter(st.character_mission_category_level_master_id for st in all_stages)
    for row in await s.rows("CharacterMission"):
        if row["characterBaseMasterId"] != base_master_id:
            continue
        m = master("character_mission_master", row["characterMissionMasterId"])
        stages = sorted(m.stages or [], key=lambda st: st.stage_order)
        available = [
            st
            for st in stages
            if categories[st.character_mission_category_level_master_id].level
            <= base["keyMissionLevel"] + 1
        ]
        pending = [
            st
            for st in available
            if row["rewardReceivedStageOrder"]
            < st.stage_order
            <= row["clearedStageOrder"]
        ]
        if not pending:
            continue
        for st in pending:
            cid = st.character_mission_category_level_master_id
            points += categories[cid].give_star_point // sizes[cid]
        claimed = max(st.stage_order for st in pending)
        # a completed category stays at its last stage until its next level unlocks
        current = next(
            (st for st in available if st.stage_order > claimed), available[-1]
        )
        completed = max(
            [
                categories[st.character_mission_category_level_master_id].level
                for st in available
                if st.stage_order <= claimed
                and not any(
                    other.stage_order > claimed
                    and other.character_mission_category_level_master_id
                    == st.character_mission_category_level_master_id
                    for other in stages
                )
            ]
            + [row["completedLevel"]]
        )
        await s.update(
            "CharacterMission",
            row,
            rewardReceivedStageOrder=claimed,
            currentStageMasterId=current.id_,
            completedLevel=completed,
        )
    rank = rank_before
    balance = points_before + points
    while True:
        level = master("character_star_rank_master", rank, "rank")
        if (
            not level
            or level.next_rank_point <= 0
            or balance < level.next_rank_point
            or not master("character_star_rank_master", rank + 1, "rank")
        ):
            break
        balance -= level.next_rank_point
        rank += 1
    await s.update("CharacterBase", base, starRank=rank, totalStarPoint=balance)
    rewards = []
    for r in cache.star_rank_reward_master:
        if (
            r.character_base_master_id == base_master_id
            and rank_before < r.rank <= rank
        ):
            group = master(
                "character_star_rank_reward_group_master",
                r.character_star_rank_reward_group_master_id,
            )
            rewards.extend(
                (int(t.thing_type), t.thing_id, t.thing_quantity)
                for t in group.rewards or []
            )
    received = await s.grant(rewards)
    return StarPointResult(
        rank_before=rank_before,
        rank_after=rank,
        star_point_before=points_before,
        star_point_after=balance,
        star_point_acquired=points,
        received_reward=received,
    )


# /api/CharacterMissions/checkInitializeMissions
@router.post(
    "/api/CharacterMissions/checkInitializeMissions",
    name="CharacterMission_CheckInitializeCharacterMissions",
)
async def character_mission_check_initialize_character_missions(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/CharacterMissions/{mCharacterBaseId}/receiveAllMission
@router.post(
    "/api/CharacterMissions/{mCharacterBaseId}/receiveAllMission",
    name="CharacterMission_ReceiveAllMissionRewards",
)
async def character_mission_receive_all_mission_rewards(
    request: Request, mCharacterBaseId: int
):
    try:
        async with transaction(request) as s:
            result = await _claim_star_rewards(s, mCharacterBaseId)
        return respond(result, present=s.present())
    except Rejected:
        return respond(StarPointResult())


# /api/CharacterMissions/BulkReceiveAllMission
@router.post(
    "/api/CharacterMissions/BulkReceiveAllMission",
    name="CharacterMission_ReceiveAllMissionRewardsAll",
)
async def character_mission_receive_all_mission_rewards_all(request: Request):
    payload = await read_request(request)
    try:
        async with transaction(request) as s:
            results = []
            for base in await s.rows("CharacterBase"):
                try:
                    result = await _claim_star_rewards(s, base["characterBaseMasterId"])
                except Rejected:
                    continue
                results.append(
                    CharacterBaseStarPointResult(
                        character_base_master_id=base["characterBaseMasterId"],
                        star_point_result=result,
                    )
                )
        return respond(results, present=s.present())
    except Rejected:
        return respond([])


# /api/CharacterMissions/{mCharacterBaseId}/receiveKeyMission
@router.post(
    "/api/CharacterMissions/{mCharacterBaseId}/receiveKeyMission",
    name="CharacterMission_ReceiveKeyMissionRewards",
)
async def character_mission_receive_key_mission_rewards(
    request: Request, mCharacterBaseId: int
):
    try:
        async with transaction(request) as s:
            row = await s.one("CharacterBase", characterBaseMasterId=mCharacterBaseId)
            if not row:
                raise Rejected()
            m = master(
                "character_key_mission_master", row["keyMissionLevel"] + 1, "level"
            )
            if not m:
                raise Rejected()
            counts = {
                r["characterMissionMasterId"]: r["currentCount"]
                for r in await s.rows("CharacterMission")
                if r["characterBaseMasterId"] == mCharacterBaseId
            }
            category_ids = {
                x.id_
                for x in cache.character_mission_category_level_master
                if x.level == m.level
            }
            complete = 0
            for category in category_ids:
                goals = [
                    (x.id_, st.goal_count)
                    for x in cache.character_mission_master
                    for st in x.stages or []
                    if st.character_mission_category_level_master_id == category
                ]
                if goals and all(counts.get(i, 0) >= g for i, g in goals):
                    complete += 1
            if complete < m.required_category_count:
                raise Rejected()
            await s.update("CharacterBase", row, keyMissionLevel=m.level)
            result = await star_points(s, mCharacterBaseId, m.give_star_point)
        return respond(result, present=s.present())
    except Rejected:
        return respond(StarPointResult())
