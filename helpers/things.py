"""Granting "things" (rewards) -- the item/currency analog of sekai's materials. A grant
either lands directly in the caller's inventory (item stock, jewels, coin) or is delivered
to the inbox as a claimable package; either way it produces a ReceivedThing describing it.
"""

import random
import time

from db.user import add_currency, create_inbox, increment_item_stock
from models import ReceivedThing
from models.enums import ThingTypes

_MICRO = 1_000_000
_INBOX_TTL_MICROS = 30 * 86400 * _MICRO


def _random_id() -> int:
    return random.randint(1_000_000, 9_999_999_999)


async def _to_inbox(
    conn, user_id, thing_type, thing_id, quantity, description
) -> ReceivedThing:
    now = int(time.time() * _MICRO)
    await conn.execute(
        create_inbox(
            user_id,
            _random_id(),
            thing_type,
            thing_id,
            quantity,
            description,
            now,
            now + _INBOX_TTL_MICROS,
        )
    )
    return ReceivedThing(
        type=thing_type, id_=thing_id, quantity=quantity, sent_inbox=True
    )


async def grant_thing(
    conn,
    user_id: int,
    thing_type: int,
    thing_id: int,
    quantity: int,
    *,
    to_inbox: bool = False,
    description=None,
) -> ReceivedThing:
    """Grant one thing. ``to_inbox`` (or any type we don't yet grant directly) sends it to
    the inbox instead of the inventory. Returns the ReceivedThing describing the grant.
    """
    thing_type = int(thing_type)
    if to_inbox:
        return await _to_inbox(
            conn, user_id, thing_type, thing_id, quantity, description
        )
    if thing_type == int(ThingTypes.Item):
        await conn.execute(increment_item_stock(user_id, thing_id, quantity))
    elif thing_type == int(ThingTypes.Jewel):
        await conn.execute(add_currency(user_id, free_jewel=quantity))
    elif thing_type == int(ThingTypes.Coin):
        await conn.execute(add_currency(user_id, coin=quantity))
    else:
        # types without a direct-grant path yet -> inbox them so nothing is silently dropped
        return await _to_inbox(
            conn, user_id, thing_type, thing_id, quantity, description
        )
    return ReceivedThing(
        type=thing_type, id_=thing_id, quantity=quantity, sent_inbox=False
    )


async def grant_things(conn, user_id: int, things, *, to_inbox: bool = False) -> list:
    """Grant many things. ``things`` items are ``(thing_type, thing_id, quantity)`` or
    ``(thing_type, thing_id, quantity, description)``. Returns the ReceivedThing[]."""
    received = []
    for thing in things:
        description = thing[3] if len(thing) > 3 else None
        received.append(
            await grant_thing(
                conn,
                user_id,
                thing[0],
                thing[1],
                thing[2],
                to_inbox=to_inbox,
                description=description,
            )
        )
    return received
