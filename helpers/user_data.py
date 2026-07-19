"""Builds the ``/api/data/user`` response (an ``IDataObject[]``) entirely from the DB.

Resolve the caller, acquire a DB connection, fetch every per-user entity
table via its ``db.user.get_<table>s`` query, and assemble the flat
MessagePack union array ``[[unionKey, [field values by Key(n)]], ...]``.

Each row (a camelCase ``<Entity>Model``) is re-encoded to ``[unionKey, [values by
Key(n)]]``: value types default to 0/false, ``DateTime`` -> msgpack timestamp,
reference/Nullable -> null.
"""

import datetime
import json
import math
import re
from typing import TYPE_CHECKING, Optional

import msgpack

from db import user as db_user
from helpers.auth import decode_jwt
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
        if isinstance(v, int):  # DB stores epoch microseconds
            return msgpack.Timestamp(v // 1_000_000, (v % 1_000_000) * 1000)
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
_REGISTRY_MAP = {_t: (_k, _g) for _t, _k, _g in _REGISTRY}


def _bearer(request) -> Optional[str]:
    auth = request.headers.get("Authorization")
    if not auth:
        return None
    return auth[7:].strip() if auth.lower().startswith("bearer ") else auth.strip()


def current_user_id(request) -> Optional[int]:
    """Resolve the caller's userId from the JWT bearer token, or None."""
    token = _bearer(request)
    return decode_jwt(token) if token else None


def data_object(type_name: str, row_model) -> list:
    """One ``IDataObject[]`` present entry ``[unionKey, [values by Key(n)]]`` from a
    DB row model (e.g. for a route's ``present``)."""
    return [IDATA_OBJECT_KEY[type_name], _to_array(type_name, row_model.model_dump())]


def empty_data_object(type_name: str) -> list:
    """A present entry with an empty value array -- some updates send a bare typed marker
    rather than the object's data (e.g. UpdateGameHintRead returns an empty GameHint).
    """
    return [IDATA_OBJECT_KEY[type_name], []]


async def build_present(app: "YumeApp", user_id: Optional[int], *updated) -> list:
    """Assemble a route's ``present`` -- the ``IDataObject[]`` diff of the resources the
    operation actually updated. Each arg names what changed: an entity type (all of the
    caller's rows of that type) or a ``(type_name, ids)`` pair to limit to specific row ids,
    e.g. ``build_present(app, uid, "User", ("Inbox", claimed_ids))``. Rows are read back
    from the DB so present reflects the post-update state. Unknown types are skipped."""
    if user_id is None:
        return []
    out: list = []
    async with app.acquire_db() as conn:
        for spec in updated:
            name, ids = spec if isinstance(spec, tuple) else (spec, None)
            entry = _REGISTRY_MAP.get(name)
            if entry is None:
                continue
            union_key, get = entry
            for row in await conn.fetch(get(user_id)):
                data = row.model_dump()
                if ids is None or data.get("id") in ids:
                    out.append([union_key, _to_array(name, data)])
    return out


_ALL_TYPES = tuple(t for t, _, _ in _REGISTRY)


def _user_data_sql() -> str:
    # one round-trip: json_agg each per-user table server-side into a single row of
    # {typeName: [rows...]} columns, every subquery sharing the $1 userId placeholder.
    parts = [
        f"(SELECT coalesce(json_agg(_r), '[]'::json) FROM ({get(0).sql}) _r) AS \"{name}\""
        for name, _key, get in _REGISTRY
    ]
    return "SELECT " + ", ".join(parts)


_USER_DATA_SQL = _user_data_sql()


async def user_data(app: "YumeApp", user_id: Optional[int]) -> list:
    """The caller's full ``IDataObject[]`` from every per-user table (for GetUserData),
    fetched in a single query."""
    if user_id is None:
        return []
    async with app.acquire_db() as conn:
        record = await conn.conn.fetchrow(_USER_DATA_SQL, user_id)
    if record is None:
        return []
    out: list = []
    for name, union_key, _get in _REGISTRY:
        value = record[name]
        rows = json.loads(value) if isinstance(value, str) else value
        for row in rows or []:
            out.append([union_key, _to_array(name, row)])
    return out
