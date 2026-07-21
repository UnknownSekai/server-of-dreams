from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from db.user import (
    get_characters,
    get_items,
    get_users,
    increment_item_stocks,
    update_character_awakening,
    update_character_level,
    update_character_sense_level,
    update_character_talent_stage,
)
from helpers.character_enhance import (
    awakening_cost,
    bloom_cost,
    bloom_rewards,
    character_master,
    max_awakening_phase,
    max_sense_level,
    max_talent_stage,
    sense_enhance_cost,
)
from helpers.character_level import (
    apply_experience,
    experience_item,
    experience_to_reach,
    level_cap,
    spend_from_pool,
)
from helpers.msgpack import fault, read_request, read_request_list, respond
from helpers.things import grant_things_consolidated, present_type
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


# /api/Characters/{characterId}/AddExperience
@router.post(
    "/api/Characters/{characterId}/AddExperience", name="Characters_AddExperience"
)
async def characters_add_experience(request: Request, characterId: int):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payloads = await read_request_list(request, UseExperienceItemsPayload)
    if user_id is None or not payloads:
        return respond(BooleanResult())

    # the client may list an item more than once, and lists the ones it isn't using at
    # quantity 0 -- fold the entries so a single stock check covers the whole batch
    use: dict = {}
    gained = 0
    for entry in payloads:
        master = experience_item(entry.item_master_id)
        if master is None:
            return respond(BooleanResult(), faults=[fault("InvalidRequest")])
        if entry.quantity <= 0:
            continue
        use[entry.item_master_id] = use.get(entry.item_master_id, 0) + entry.quantity
        gained += master.acquirable_experience * entry.quantity
    if not use:
        return respond(BooleanResult())

    async with app.acquire_db() as conn, conn.transaction():
        user = await conn.fetchrow(get_users(user_id))
        character = await _character(conn, user_id, characterId)
        if user is None or character is None:
            return respond(BooleanResult(), faults=[fault("InvalidRequest")])
        if not await _pay_items(conn, user_id, use):
            return respond(BooleanResult(), faults=[fault("NotEnoughThing")])

        # a character sitting at the cap still takes the exp -- it banks against the next
        # player rank uncap instead of being thrown away
        level, experience = apply_experience(
            character.level, character.currentExperience, gained, level_cap(user)
        )
        await conn.execute(
            update_character_level(user_id, characterId, level, experience)
        )

    present = await build_present(
        app, user_id, ("Character", {characterId}), ("Item", set(use))
    )
    return respond(BooleanResult(is_success=True), present=present)


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
    """Bloom a character's talent up to ``stageTo``, paying for every stage on the way."""
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payload = {}  # no payload -- the target stage is a path segment
    if user_id is None:
        return respond(BooleanResult())

    rewards: list = []
    received: list = []
    async with app.acquire_db() as conn, conn.transaction():
        character = await _character(conn, user_id, characterId)
        master = character_master(character.characterMasterId) if character else None
        if character is None or master is None:
            return respond(BooleanResult(), faults=[fault("InvalidRequest")])
        if not character.talentStage < stageTo <= max_talent_stage(master):
            return respond(BooleanResult(), faults=[fault("InvalidRequest")])

        stock = await _item_stock(conn, user_id)
        # what the bill is depends on what's owned -- own pieces first, generic for the rest
        cost = bloom_cost(master, character.talentStage, stageTo, stock)
        if cost is None or not await _pay_items(conn, user_id, cost, stock):
            return respond(BooleanResult(), faults=[fault("NotEnoughThing")])
        await conn.execute(update_character_talent_stage(user_id, characterId, stageTo))

        rewards = bloom_rewards(master, character.talentStage, stageTo)
        if rewards:
            received = await grant_things_consolidated(conn, user_id, rewards)

    refresh = {present_type(int(r.type)) for r in received}
    refresh.discard(None)
    refresh.discard("Item")  # the item ids are reported alongside the ones just spent
    items = set(cost) | {tid for tt, tid, _ in rewards if tt == int(ThingTypes.Item)}
    present = await build_present(
        app,
        user_id,
        ("Character", {characterId}),
        ("Item", items),
        *sorted(refresh),
    )
    return respond(BooleanResult(is_success=True), present=present)


# /api/Characters/BulkLevelUp
@router.post("/api/Characters/BulkLevelUp", name="Characters_BulkLevelUp")
async def characters_bulk_level_up(request: Request):
    """Spend the caller's exp items across several characters at once, each one taken as far
    as the player rank cap allows."""
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payloads = await read_request_list(request, BulkLevelUpPayload)
    if user_id is None or not payloads:
        return respond(BooleanResult())

    leveled: set = set()
    spent: dict = {}
    async with app.acquire_db() as conn, conn.transaction():
        user = await conn.fetchrow(get_users(user_id))
        if user is None:
            return respond(BooleanResult(), faults=[fault("InvalidRequest")])
        cap = level_cap(user)
        characters = {c.id: c for c in await conn.fetch(get_characters(user_id))}
        stock = _experience_pool(await _item_stock(conn, user_id))

        # every entry draws on the one pool, so `order` is who gets first claim on it
        for entry in sorted(payloads, key=lambda p: p.order):
            character = characters.get(entry.character_id)
            if character is None or character.level >= cap:
                continue
            spend = spend_from_pool(
                stock,
                experience_to_reach(character.level, character.currentExperience, cap),
            )
            gained = 0
            for item_master_id, quantity in spend.items():
                stock[item_master_id] -= quantity
                spent[item_master_id] = spent.get(item_master_id, 0) + quantity
                master = experience_item(item_master_id)
                gained += master.acquirable_experience * quantity if master else 0
            if not gained:
                continue
            level, experience = apply_experience(
                character.level, character.currentExperience, gained, cap
            )
            await conn.execute(
                update_character_level(user_id, character.id, level, experience)
            )
            leveled.add(character.id)

        if not leveled:  # nothing affordable -- no items were touched either
            return respond(BooleanResult())
        await conn.execute(
            increment_item_stocks(user_id, [(i, -q) for i, q in spent.items()])
        )

    present = await build_present(
        app, user_id, ("Character", leveled), ("Item", set(spent))
    )
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
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payload = {}  # no payload -- target level and sense are path/query
    if user_id is None:
        return respond(BooleanResult())
    secondary = priority == int(SenseFirePriority.Secondary)

    async with app.acquire_db() as conn, conn.transaction():
        character = await _character(conn, user_id, characterId)
        master = character_master(character.characterMasterId) if character else None
        if character is None or master is None:
            return respond(BooleanResult(), faults=[fault("InvalidRequest")])
        if secondary and master.secondary_sense_master_id is None:
            return respond(BooleanResult(), faults=[fault("InvalidRequest")])
        # the cost table starts at level 1, and so does a sense -- a secondary that was never
        # initialised reads 0 in its column but is standing at the same first step
        current = max(
            1, character.secondarySenseLevel if secondary else character.senseLevel
        )
        if not current < levelTo <= max_sense_level(master):
            return respond(BooleanResult(), faults=[fault("InvalidRequest")])

        cost = sense_enhance_cost(master, current, levelTo)
        if cost is None:
            return respond(BooleanResult(), faults=[fault("InvalidRequest")])
        if not await _pay_items(conn, user_id, cost):
            return respond(BooleanResult(), faults=[fault("NotEnoughThing")])
        await conn.execute(
            update_character_sense_level(user_id, characterId, levelTo, secondary)
        )

    present = await build_present(
        app, user_id, ("Character", {characterId}), ("Item", set(cost))
    )
    return respond(BooleanResult(is_success=True), present=present)


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
    app: YumeApp = request.app
    payload = {}  # no payload
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
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Characters/Portal/SetCharacter
@router.post(
    "/api/Characters/Portal/SetCharacter", name="Characters_SetPortalMCharacter"
)
async def characters_set_portal_mcharacter(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, ActorPortalCharacterPayload)
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
