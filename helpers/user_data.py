"""Builds the ``/api/data/user`` response (an ``IDataObject[]``) entirely from the DB.

Mirrors sekai-api-emulator's ``get_save_data``: resolve the caller, acquire a DB
connection, fetch every per-user entity table via its ``db.user.get_<table>s``
query, and assemble the flat MessagePack union array
``[[unionKey, [field values by Key(n)]], ...]``. Returns an empty array when the
database isn't set up or the user has no rows.

Each row (a camelCase ``<Entity>Model``) is re-encoded to ``[unionKey, [values by
Key(n)]]``: value types default to 0/false, ``DateTime`` -> msgpack timestamp,
reference/Nullable -> null.
"""

import datetime
import math
import re
from typing import TYPE_CHECKING, Optional

import msgpack

from db import account as db_account, user as db_user
from helpers.msgpack import _zero
from models.keys import KEYS
from models.unions import IDATA_OBJECT_KEY

if TYPE_CHECKING:
    from core import YumeApp

_UNIX = datetime.datetime(1970, 1, 1)


def iso_to_timestamp(s: str) -> msgpack.Timestamp:
    date, _, frac = s.partition(".")
    dt = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    nanos = int(frac[:7].ljust(7, "0")) * 100 if frac else 0
    total = (dt - _UNIX).total_seconds()
    secs = int(math.floor(total))
    return msgpack.Timestamp(secs, nanos)


def _camel(attr: str) -> str:
    parts = attr.rstrip("_").split("_")
    return parts[0] + "".join(p[:1].upper() + p[1:] for p in parts[1:])


def _table(type_name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", type_name).lower()


_CAMELMAP: dict = {}


def _camelmap(type_name: str) -> dict:
    if type_name not in _CAMELMAP:
        _CAMELMAP[type_name] = {
            _camel(attr): (key, base, arr, kind, nn)
            for key, attr, base, arr, kind, nn in KEYS[type_name]
        }
    return _CAMELMAP[type_name]


def _conv(base, is_array, kind, v):
    if v is None:
        return None
    if is_array:
        return [_conv(base, False, kind, x) for x in v]
    if kind == "model":
        return _to_array(base, v) if isinstance(v, dict) else v
    if kind == "enum":
        return int(v)
    if base == "DateTime":
        return iso_to_timestamp(v) if isinstance(v, str) else v
    return v


def _to_array(type_name: str, value: dict) -> list:
    keys = KEYS[type_name]
    if not keys:
        return []
    arr = [None] * (max(k[0] for k in keys) + 1)
    cm = _camelmap(type_name)
    for camel, val in value.items():
        info = cm.get(camel)
        if info:
            key, base, is_array, kind, nn = info
            arr[key] = _conv(base, is_array, kind, val)
    for key, _attr, base, _is_array, kind, nn in keys:
        if arr[key] is None and not nn:
            arr[key] = _zero(base, kind)
    return arr


# entity type -> (unionKey, db.user.get_<table>s query builder), for every entity
# that has both a union discriminator and a per-user table.
_REGISTRY = []
for _type, _key in IDATA_OBJECT_KEY.items():
    if _type in KEYS and KEYS[_type]:
        _get = getattr(db_user, f"get_{_table(_type)}s", None)
        if _get is not None:
            _REGISTRY.append((_type, _key, _get))


def _bearer(request) -> Optional[str]:
    auth = request.headers.get("Authorization")
    if not auth:
        return None
    return auth[7:].strip() if auth.lower().startswith("bearer ") else auth.strip()


async def current_user_id(app: "YumeApp", request) -> Optional[int]:
    """Resolve the caller's userId from the API token, or None."""
    token = _bearer(request)
    if not app.is_setup or not token:
        return None
    async with app.acquire_db() as conn:
        account = await conn.fetchrow(db_account.get_account_by_token(token))
    return account.userId if account else None


async def user_data(app: "YumeApp", user_id: Optional[int]) -> list:
    """Assemble the caller's full ``IDataObject[]`` from every per-user table."""
    if user_id is None or not app.is_setup:
        return []
    out: list = []
    async with app.acquire_db() as conn:
        for type_name, union_key, get in _REGISTRY:
            for row in await conn.fetch(get(user_id)):
                out.append([union_key, _to_array(type_name, row.model_dump())])
    return out
