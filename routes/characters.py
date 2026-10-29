import math
from collections import Counter
from typing import Optional

from fastapi import APIRouter, Request

from core import YumeApp
from db.user import (
    get_characters,
    get_items,
    get_user_bonuss,
    get_users,
    increment_item_stocks,
    update_character_awakening,
    update_character_level,
)
from helpers import game_state as gs
from helpers.cache import cache
from helpers.character_enhance import (
    awakening_cost,
    bloom_rewards,
    character_master,
    max_awakening_phase,
    max_sense_level,
    max_talent_stage,
    sense_enhance_cost,
)
from helpers.character_level import (
    character_rarity,
    experience_item,
    experience_to_reach,
    level_cap,
    released_max_level,
    spend_from_pool,
)
from helpers.msgpack import fault, read_request, read_request_list, respond
from helpers.user_data import build_present, current_user_id
from models import *

router = APIRouter(tags=["Characters"])


async def _character(conn, user_id: int, character_id: int):
    """One of the caller's characters by id, or None."""
    return next(
        (c for c in await conn.fetch(get_characters(user_id)) if c.id == character_id),
        None,
    )


async def _item_stock(conn, user_id: int) -> dict:
    """Everything the caller owns, ``{itemMasterId: stock}``."""
    return {i.itemMasterId: i.stock for i in await conn.fetch(get_items(user_id))}


async def _pay_items(
    conn, user_id: int, cost: dict, stock: Optional[dict] = None
) -> bool:
    """Charge a whole item bill in one statement. Writes nothing unless every line of it is
    affordable, so an enhancement can't half-charge and then fail."""
    if not cost:
        return False
    if stock is None:
        stock = await _item_stock(conn, user_id)
    if any(stock.get(item, 0) < quantity for item, quantity in cost.items()):
        return False
    await conn.execute(
        increment_item_stocks(user_id, [(i, -q) for i, q in cost.items()])
    )
    return True


def _experience_pool(stock: dict) -> dict:
    """The exp items out of a stock -- what a level-up can spend."""
    return {
        item: owned
        for item, owned in stock.items()
        if experience_item(item) is not None
    }


def _actor_item_experience(costs: dict, bonus: float) -> int:
    # official one/two-item captures round each item before multiplying quantity
    return sum(
        n * math.floor(experience_item(i).acquirable_experience * (1 + bonus / 100))
        for i, n in costs.items()
    )


def _actor_experience(level: int, current: int, gained: int, cap: int, rarity):
    # the master curve is for rarity 4; lower rarities pay a fraction of each level's step
    factor = {1: 0.3, 2: 0.5, 3: 0.8, 4: 1.0}[int(rarity)]
    levels = {x.level: x.experience_to_level_up for x in cache.character_level_master}
    experience = current + gained
    while level < cap:
        need = math.floor(levels[level] * factor)
        if need <= 0 or experience < need:
            break
        experience -= need
        level += 1
    return level, experience


# /api/Characters/{characterId}/AddExperience
@router.post(
    "/api/Characters/{characterId}/AddExperience", name="Characters_AddExperience"
)
async def characters_add_experience(request: Request, characterId: int):
    try:
        payloads = await read_request_list(request, UseExperienceItemsPayload)
        costs: Counter = Counter()
        raw = 0
        bonus_gain = 0
        for entry in payloads or []:
            item = experience_item(entry.item_master_id)
            if not item or entry.quantity < 0:
                raise gs.Rejected()
            costs[entry.item_master_id] += entry.quantity
            raw += item.acquirable_experience * entry.quantity
            bonus_gain += item.acquirable_experience_bonus * entry.quantity
        if raw <= 0:
            raise gs.Rejected()
        async with gs.transaction(request) as s:
            row = await s.one("Character", id=characterId)
            user = await s.one("User")
            bonus = await s.one("UserBonus")
            if not row or not user or not bonus:
                raise gs.Rejected()
            cm = character_master(row["characterMasterId"])
            cap = min(user["playerRankLimit"], released_max_level())
            if row["level"] >= cap:
                raise gs.Rejected()
            gained = _actor_item_experience(costs, bonus["experienceBonus"])
            level, exp = _actor_experience(
                row["level"], row["currentExperience"], gained, cap, cm.rarity
            )
            delta = level - row["level"]
            await s.pay(costs)
            await s.update("Character", row, level=level, currentExperience=exp)
            await s.update(
                "UserBonus",
                bonus,
                experienceBonus=gs.f32(bonus["experienceBonus"] + bonus_gain),
            )
            await gs.level_missions(s, cm, delta, level)
        return respond(BooleanResult(is_success=True), present=s.present())
    except gs.NotEnough:
        return respond(BooleanResult(), faults=[fault("NotEnoughThing")])
    except gs.Rejected:
        return respond(BooleanResult(), faults=[fault("InvalidRequest")])


# /api/Characters/{characterId}/Awaken
@router.post("/api/Characters/{characterId}/Awaken", name="Characters_Awaken")
async def characters_awaken(request: Request, characterId: int):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payload = {}  # no payload -- the character is the whole request
    if user_id is None:
        return respond(BooleanResult())

    async with app.acquire_db() as conn, conn.transaction():
        character = await _character(conn, user_id, characterId)
        master = character_master(character.characterMasterId) if character else None
        if character is None or master is None:
            return respond(BooleanResult(), faults=[fault("InvalidRequest")])
        # 42 characters carry no awakening group at all, so their max phase is 0
        if character.awakeningPhase >= max_awakening_phase(master):
            return respond(BooleanResult(), faults=[fault("InvalidRequest")])
        cost = awakening_cost(master, character.awakeningPhase)
        if cost is None:
            return respond(BooleanResult(), faults=[fault("InvalidRequest")])
        if not await _pay_items(conn, user_id, cost):
            return respond(BooleanResult(), faults=[fault("NotEnoughThing")])
        await conn.execute(
            update_character_awakening(
                user_id, characterId, character.awakeningPhase + 1
            )
        )

    present = await build_present(
        app, user_id, ("Character", {characterId}), ("Item", set(cost))
    )
    return respond(BooleanResult(is_success=True), present=present)


# /api/Characters/{characterId}/BloomTalent/{stageTo}
@router.post(
    "/api/Characters/{characterId}/BloomTalent/{stageTo}", name="Characters_BloomTalent"
)
async def characters_bloom_talent(request: Request, characterId: int, stageTo: int):
    """Bloom a character's talent up to ``stageTo``, paying for every stage on the way.
    Owned pieces are spent first, generic pieces cover any shortfall."""
    from helpers.character_enhance import _bloom_step, _generic_piece, _piece

    try:
        async with gs.transaction(request) as s:
            row = await s.one("Character", id=characterId)
            if not row:
                raise gs.Rejected()
            cm = character_master(row["characterMasterId"])
            if not cm or not row["talentStage"] < stageTo <= max_talent_stage(cm):
                raise gs.Rejected()
            stock = {r["itemMasterId"]: r["stock"] for r in await s.rows("Item")}
            costs: Counter = Counter()
            remaining = stock.copy()
            for stage in range(row["talentStage"], stageTo):
                step = _bloom_step(cm.rarity, stage)
                piece = _piece(cm.id_, step.talent_bloom_item_type)
                own = min(
                    remaining.get(piece.item_master_id, 0), step.required_piece_amount
                )
                costs[piece.item_master_id] += own
                remaining[piece.item_master_id] = (
                    remaining.get(piece.item_master_id, 0) - own
                )
                short = step.required_piece_amount - own
                if short:
                    generic, _ = _generic_piece(cm, step, piece)
                    if not generic or cm.forbid_generic_item_bloom:
                        raise gs.Rejected()
                    costs[generic] += short
                if step.required_item_master_id:
                    costs[step.required_item_master_id] += step.required_item_amount or 0
            await s.pay(costs)
            delta = stageTo - row["talentStage"]
            rewards = bloom_rewards(cm, row["talentStage"], stageTo)
            await s.update("Character", row, talentStage=stageTo)
            await s.grant(rewards)
            await gs.character_progress(s, cm.character_base_master_id, 6, delta)
        return respond(BooleanResult(is_success=True), present=s.present())
    except gs.Rejected:
        return respond(BooleanResult())


# /api/Characters/BulkLevelUp
@router.post("/api/Characters/BulkLevelUp", name="Characters_BulkLevelUp")
async def characters_bulk_level_up(request: Request):
    """Spend the caller's exp items across several characters at once, each one taken as far
    as the player rank cap allows."""
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payloads = await read_request_list(request, BulkLevelUpPayload)
    if user_id is None or not payloads:
        return respond(BooleanResult(), faults=[fault("InvalidRequest")])

    leveled: set = set()
    spent: dict = {}
    bonus_gain = 0.0
    needed_any = False
    async with app.acquire_db() as conn, conn.transaction():
        user = await conn.fetchrow(get_users(user_id))
        bonus = await conn.fetchrow(get_user_bonuss(user_id))
        if user is None or bonus is None:
            return respond(BooleanResult(), faults=[fault("InvalidRequest")])
        cap = level_cap(user)
        characters = {c.id: c for c in await conn.fetch(get_characters(user_id))}
        stock = _experience_pool(await _item_stock(conn, user_id))

        # every entry draws on the one pool, so `order` is who gets first claim on it
        for entry in sorted(payloads, key=lambda p: p.order):
            character = characters.get(entry.character_id)
            if character is None or character.level >= cap:
                continue
            rarity = character_rarity(character.characterMasterId)
            needed = experience_to_reach(
                character.level, character.currentExperience, cap, rarity
            )
            if needed <= 0:
                continue
            needed_any = True
            spend = spend_from_pool(stock, needed, bonus.experienceBonus)
            gained = _actor_item_experience(spend, bonus.experienceBonus)
            if not spend or gained <= 0:
                continue
            for item_master_id, quantity in spend.items():
                stock[item_master_id] -= quantity
                spent[item_master_id] = spent.get(item_master_id, 0) + quantity
                master = experience_item(item_master_id)
                if master:
                    bonus_gain += master.acquirable_experience_bonus * quantity
            level, experience = _actor_experience(
                character.level, character.currentExperience, gained, cap, rarity
            )
            await conn.execute(
                update_character_level(user_id, character.id, level, experience)
            )
            leveled.add(character.id)

        if not leveled:  # nothing affordable -- no items were touched either
            faults = [fault("NotEnoughThing" if needed_any else "InvalidRequest")]
            return respond(BooleanResult(), faults=faults)
        await conn.execute(
            increment_item_stocks(user_id, [(i, -q) for i, q in spent.items()])
        )
        if bonus_gain:
            await conn.conn.execute(
                'UPDATE "user_bonus" SET "experienceBonus"=$1 '
                'WHERE "userId"=$2 AND "id"=$3',
                gs.f32(bonus.experienceBonus + bonus_gain),
                user_id,
                bonus.id,
            )
        spent_ids = {
            item.id
            for item in await conn.fetch(get_items(user_id))
            if item.itemMasterId in spent
        }

    present_args = [("Character", leveled), ("Item", spent_ids)]
    if bonus_gain:
        present_args.append("UserBonus")
    present = await build_present(app, user_id, *present_args)
    return respond(BooleanResult(is_success=True), present=present)


# /api/Characters/{characterId}/EnhanceSenseLevel/{levelTo}?priority=
@router.post(
    "/api/Characters/{characterId}/EnhanceSenseLevel/{levelTo}",
    name="Characters_EnhanceSenseLevel",
)
async def characters_enhance_sense_level(
    request: Request, characterId: int, levelTo: int, priority: Optional[int] = None
):
    """Raise a sense to ``levelTo``. ``priority`` picks which of a dual character's two
    senses is being enhanced -- they level independently, out of the same item group."""
    pr = priority if priority is not None else 1
    try:
        async with gs.transaction(request) as s:
            row = await s.one("Character", id=characterId)
            if not row or pr not in (1, 2):
                raise gs.Rejected()
            cm = character_master(row["characterMasterId"])
            field = "senseLevel" if pr == 1 else "secondarySenseLevel"
            base = (
                cm.character_base_master_id
                if pr == 1
                else cm.secondary_character_base_master_id
            )
            # the cost table starts at level 1, and so does a sense -- a secondary that was
            # never initialised reads 0 but stands at that same first step, so clamp to 1
            current = max(1, row[field])
            if not base or not current < levelTo <= max_sense_level(cm):
                raise gs.Rejected()
            costs = sense_enhance_cost(cm, current, levelTo)
            if not costs:
                raise gs.Rejected()
            delta = levelTo - current
            await s.pay(costs)
            await s.update("Character", row, **{field: levelTo})
            await gs.character_progress(s, base, 5, delta)
            if levelTo >= 2:
                await gs.mission_progress(s, 14, create=True, absolute=1)
        return respond(BooleanResult(is_success=True), present=s.present())
    except gs.Rejected:
        return respond(BooleanResult())


# /api/Characters/LinkCharacter?mCharacterBaseId=&linkedMCharacterBaseId=
@router.post("/api/Characters/LinkCharacter", name="Characters_LinkCharacter")
async def characters_link_character(
    request: Request,
    mCharacterBaseId: Optional[int] = None,
    linkedMCharacterBaseId: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])


# /api/Characters/ReceiveLinkCharacterReward?mCharacterBaseId=
@router.post(
    "/api/Characters/ReceiveLinkCharacterReward",
    name="Characters_ReceiveLinkCharacterReward",
)
async def characters_receive_link_character_reward(
    request: Request, mCharacterBaseId: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])


# /api/Characters/{characterMasterId}/ReleaseSideStory?order=
@router.post(
    "/api/Characters/{characterMasterId}/ReleaseSideStory",
    name="Characters_ReleaseSideStory",
)
async def characters_release_side_story(
    request: Request, characterMasterId: int, order: Optional[int] = None
):
    target = order if order is not None else 1
    try:
        async with gs.transaction(request) as s:
            row = await s.one("Character", characterMasterId=characterMasterId)
            cm = character_master(characterMasterId)
            episode = next(
                (
                    e
                    for e in cache.character_episode_master
                    if e.character_master_id == characterMasterId
                    and int(e.episode_order) == target
                ),
                None,
            )
            if (
                not row
                or not cm
                or not episode
                or row["level"] < episode.required_character_level
                or target != row["releasedEpisodeOrder"] + 1
            ):
                raise gs.Rejected()
            gid = (
                cm.first_episode_release_item_group_id
                if target == 1
                else cm.second_episode_release_item_group_id
            )
            group = gs.master("character_episode_release_item_group_master", gid)
            if not group:
                raise gs.Rejected()
            costs: Counter = Counter()
            for i in group.items or []:
                if i.order == target:
                    costs[i.item_master_id] += i.required_quantity
            if not costs:
                raise gs.Rejected()
            await s.pay(costs)
            await s.update("Character", row, releasedEpisodeOrder=target)
        return respond(BooleanResult(is_success=True), present=s.present())
    except gs.Rejected:
        return respond(BooleanResult())


# /api/Characters/SetFavorite
@router.post("/api/Characters/SetFavorite", name="Characters_SetCharacterFavorite")
async def characters_set_character_favorite(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, CharacterFavoritePayload)
    return respond(BooleanResult())


# /api/CharacterBases/{characterBaseMasterId}/SetCostume/{costumeMasterId}
@router.post(
    "/api/CharacterBases/{characterBaseMasterId}/SetCostume/{costumeMasterId}",
    name="Characters_SetCostume",
)
async def characters_set_costume(
    request: Request, characterBaseMasterId: int, costumeMasterId: int
):
    try:
        async with gs.transaction(request) as s:
            await gs.costume_owned(s, characterBaseMasterId, costumeMasterId)
            base = await s.one(
                "CharacterBase", characterBaseMasterId=characterBaseMasterId
            )
            await s.update("CharacterBase", base, costumeMasterId=costumeMasterId)
        return respond(BooleanResult(is_success=True), present=s.present())
    except gs.Rejected:
        return respond(BooleanResult())


# /api/Characters/Portal/SetCharacter
@router.post(
    "/api/Characters/Portal/SetCharacter", name="Characters_SetPortalMCharacter"
)
async def characters_set_portal_mcharacter(request: Request):
    try:
        payload = await read_request(request, ActorPortalCharacterPayload)
        if payload is None:
            raise gs.Rejected()
        async with gs.transaction(request) as s:
            if not character_master(payload.character_id) or not await s.one(
                "Character", characterMasterId=payload.character_id
            ):
                raise gs.Rejected()
            base = await s.one(
                "CharacterBase", characterBaseMasterId=payload.character_base_id
            )
            await s.update(
                "CharacterBase",
                base,
                portalCharacterId=payload.character_id,
                portalDisplayAwakeningStatus=bool(payload.is_awakening),
            )
        return respond(BooleanResult(is_success=True), present=s.present())
    except gs.Rejected:
        return respond(BooleanResult())


# /api/Characters/{characterId}/SwitchCharacterDisplayAwakeningStatusAsync
@router.post(
    "/api/Characters/{characterId}/SwitchCharacterDisplayAwakeningStatusAsync",
    name="Characters_SwitchCharacterDisplayAwakeningStatus",
)
async def characters_switch_character_display_awakening_status(
    request: Request, characterId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Characters/UpdateSelectionType?characterId=&selectionType=
@router.post(
    "/api/Characters/UpdateSelectionType", name="Characters_UpdateSelectionType"
)
async def characters_update_selection_type(
    request: Request,
    characterId: Optional[int] = None,
    selectionType: Optional[int] = None,
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())
