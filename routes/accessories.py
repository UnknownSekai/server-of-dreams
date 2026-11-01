from typing import Optional

from fastapi import APIRouter, Request

from core import YumeApp
from db.user import get_accessorys, get_currencys, update_accessory_level
from helpers.cache import cache
from helpers.costs import item_stock, pay_coin, pay_items
from helpers.msgpack import fault, read_request, respond
from helpers.user_data import build_present, current_user_id
from models import *

router = APIRouter(tags=["Accessories"])

_ACCESSORY_MASTERS: dict = {}
_ACCESSORY_PATTERN_GROUPS: dict = {}


def _accessory_master(master_id: int):
    if not _ACCESSORY_MASTERS:
        _ACCESSORY_MASTERS.update({m.id_: m for m in cache.accessory_master})
    return _ACCESSORY_MASTERS.get(master_id)


def _pattern_group(group_id: int):
    if not _ACCESSORY_PATTERN_GROUPS:
        _ACCESSORY_PATTERN_GROUPS.update(
            {g.id_: g for g in cache.accessory_level_pattern_group_master}
        )
    return _ACCESSORY_PATTERN_GROUPS.get(group_id)


def _level_cost(group, from_level: int, to_level: int):
    """Coin + item bill to raise an accessory from ``from_level`` to ``to_level``.

    Each ``AccessoryLevelPatternMaster`` row's ``level`` is the *source* level of one
    step (levels 1..9 cover 1->2 .. 9->10), so a jump sums every step in between.
    Returns ``(coin, {itemMasterId: quantity})`` or ``None`` if a step is missing.
    """
    by_level = {p.level: p for p in (group.patterns or [])}
    coin = 0
    items: dict = {}
    for level in range(from_level, to_level):
        pattern = by_level.get(level)
        if pattern is None:
            return None
        coin += pattern.required_coin
        for entry in pattern.items or []:
            items[entry.item_master_id] = (
                items.get(entry.item_master_id, 0) + entry.quantity
            )
    return coin, items


# /api/Accessories/IncreaseAcquirableAccessoryLimit?toPhase=
@router.post(
    "/api/Accessories/IncreaseAcquirableAccessoryLimit",
    name="Accessories_IncreaseAcquirableAccessoryLimit",
)
async def accessories_increase_acquirable_accessory_limit(
    request: Request, toPhase: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Accessories/{uAccessoryId}/LevelUp/{levelTo}
@router.post(
    "/api/Accessories/{uAccessoryId}/LevelUp/{levelTo}", name="Accessories_LevelUp"
)
async def accessories_level_up(request: Request, uAccessoryId: int, levelTo: int):
    app: YumeApp = request.app
    user_id = current_user_id(request)
    payload = {}  # no payload -- the accessory and target level are path segments
    if user_id is None:
        return respond(BooleanResult())

    async with app.acquire_db() as conn, conn.transaction():
        accessory = next(
            (
                a
                for a in await conn.fetch(get_accessorys(user_id))
                if a.id == uAccessoryId
            ),
            None,
        )
        master = _accessory_master(accessory.accessoryMasterId) if accessory else None
        if accessory is None or master is None:
            return respond(BooleanResult(), faults=[fault("InvalidRequest")])
        group = _pattern_group(master.accessory_level_pattern_group_id)
        if group is None or not accessory.level < levelTo <= master.max_level:
            return respond(BooleanResult(), faults=[fault("InvalidRequest")])
        cost = _level_cost(group, accessory.level, levelTo)
        if cost is None:
            return respond(BooleanResult(), faults=[fault("InvalidRequest")])
        coin, items = cost
        # check the whole bill (coin + items) before charging anything, so a partial
        # charge can't commit when only one side is affordable
        stock = await item_stock(conn, user_id)
        currency = next(iter(await conn.fetch(get_currencys(user_id))), None)
        if (currency is None or currency.coin < coin) or any(
            stock.get(i, 0) < q for i, q in items.items()
        ):
            return respond(BooleanResult(), faults=[fault("NotEnoughThing")])
        await pay_coin(conn, user_id, coin)
        await pay_items(conn, user_id, items, stock)
        await conn.execute(update_accessory_level(user_id, uAccessoryId, levelTo))

    updates = [("Accessory", {uAccessoryId}), ("Item", set(items))]
    if coin:
        updates.append("Currency")
    present = await build_present(app, user_id, *updates)
    return respond(BooleanResult(is_success=True), present=present)


# /api/Accessories/Sell
@router.post("/api/Accessories/Sell", name="Accessories_Sell")
async def accessories_sell(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, SellAccessoryPayload)
    return respond(BooleanResult())


# /api/Accessories/SetAccessoryAutoSell?rarityFlag=
@router.post(
    "/api/Accessories/SetAccessoryAutoSell", name="Accessories_SetAccessoryAutoSell"
)
async def accessories_set_accessory_auto_sell(
    request: Request, rarityFlag: Optional[int] = None
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Accessories/SetFavorite
@router.post("/api/Accessories/SetFavorite", name="Accessories_SetAccessoryFavorite")
async def accessories_set_accessory_favorite(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, AccessoryFavoritePayload)
    return respond(BooleanResult())


# /api/Accessories/{accessoryId}/SwitchLock
@router.post("/api/Accessories/{accessoryId}/SwitchLock", name="Accessories_SwitchLock")
async def accessories_switch_lock(request: Request, accessoryId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())
