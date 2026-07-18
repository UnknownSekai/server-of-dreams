"""MessagePack helpers mimicking MessagePack-CSharp (the game's serializer).

C# ``[MessagePackObject]`` + ``[Key(int)]`` serialize as an **array indexed by
key** (gaps -> nil), enums as their integer value, strings as str, byte[] as bin.
So: ``msgpack.packb(array, use_bin_type=True)`` /
``msgpack.unpackb(data, raw=False, strict_map_key=False)``.

Responses use the game's common envelope: five concatenated msgpack objects read
by ``MessagePackStreamReader`` in order — ``Fault[]``, ``TResult``,
``IDataObject[]`` (present), ``DeletedDataObject[]``, ``INotificationObject[]``.
Requests are a single msgpack object (the payload array).
"""

from enum import IntEnum

import msgpack
from fastapi import HTTPException, Request, Response
from pydantic import ValidationError

import models
from models.keys import KEYS
from helpers.headers import response_headers

_PACK = dict(use_bin_type=True)
_UNPACK = dict(raw=False, strict_map_key=False)


def _encode(base, is_array, kind, v):
    if v is None:
        return None
    if is_array:
        return [_encode(base, False, kind, x) for x in v]
    if kind == "model":
        return to_wire(v)
    if kind == "enum":
        return int(v)
    return v


def to_wire(obj):
    if obj is None:
        return None
    if isinstance(obj, (list, tuple)):
        return [to_wire(x) for x in obj]
    name = type(obj).__name__
    if name in KEYS:
        fields = KEYS[name]
        arr = [None] * ((max(f[0] for f in fields) + 1) if fields else 0)
        for key, fn, base, is_array, kind in fields:
            arr[key] = _encode(base, is_array, kind, getattr(obj, fn, None))
        return arr
    if isinstance(obj, IntEnum):
        return int(obj)
    return obj


def _decode(base, is_array, kind, v):
    if v is None:
        return None
    if is_array:
        return (
            [_decode(base, False, kind, x) for x in v]
            if isinstance(v, (list, tuple))
            else v
        )
    if kind == "model":
        return from_array(base, v)
    return v


def from_array(name, arr):
    if name is None or name not in KEYS or not isinstance(arr, (list, tuple)):
        return arr
    kwargs = {}
    for key, fn, base, is_array, kind in KEYS[name]:
        kwargs[fn] = _decode(base, is_array, kind, arr[key] if key < len(arr) else None)
    return getattr(models, name)(**kwargs)


def pack(value) -> bytes:
    return msgpack.packb(to_wire(value), **_PACK) or b""


def unpack(data):
    return msgpack.unpackb(data, **_UNPACK)


class MsgpackResponse(Response):
    media_type = "application/x-msgpack"


def common_response(
    result, faults=None, present=None, deleted=None, notifications=None
) -> MsgpackResponse:
    body = b"".join(
        [
            pack(faults or []),
            pack(result),
            pack(present or []),
            pack(deleted or []),
            pack(notifications or []),
        ]
    )
    return MsgpackResponse(content=body, headers=response_headers())


def raw_response(result) -> MsgpackResponse:
    return MsgpackResponse(content=pack(result), headers=response_headers())


def fault(error_code: str, message: str = "", stack_trace: str = "") -> list:
    return [error_code, message, stack_trace]


respond = common_response


async def read_request(request: Request, model_name=None):
    raw = await request.body()
    if not raw:
        return None
    try:
        decoded = unpack(raw)
    except Exception:
        return None
    if model_name is None:
        return decoded
    try:
        return from_array(model_name, decoded)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors())
