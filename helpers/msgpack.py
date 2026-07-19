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

import datetime
from enum import IntEnum
from typing import Any, Optional, Type, TypeVar, Union, overload

import lz4.block
import msgpack
from fastapi import HTTPException, Request, Response
from pydantic import BaseModel, ValidationError

import models
from models.keys import KEYS
from helpers.headers import response_headers

T = TypeVar("T", bound=BaseModel)

_PACK = dict(use_bin_type=True)
_UNPACK = dict(raw=False, strict_map_key=False)


_INT_TYPES = {
    "byte",
    "sbyte",
    "short",
    "ushort",
    "int",
    "uint",
    "long",
    "ulong",
    "char",
}
_FLOAT_TYPES = {"float", "double", "decimal"}
# C# default(DateTime) == DateTime.MinValue (0001-01-01): this many seconds before the Unix epoch.
DATETIME_MIN = msgpack.Timestamp(-62135596800, 0)
_EPOCH_UTC = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)


def ts_to_iso(ts: msgpack.Timestamp) -> str:
    dt = _EPOCH_UTC + datetime.timedelta(
        seconds=ts.seconds, microseconds=ts.nanoseconds // 1000
    )
    return dt.isoformat()


def iso_to_ts(s: str) -> msgpack.Timestamp:
    if not s:
        return DATETIME_MIN
    dt = datetime.datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    total_us = (dt - _EPOCH_UTC) // datetime.timedelta(microseconds=1)
    secs, micros = divmod(total_us, 1_000_000)
    return msgpack.Timestamp(secs, micros * 1000)


def _zero(base, kind):
    # non-nullable C# value types serialize as default(T); the client reads them
    # with ReadInt32/ReadInt64/etc. which throw on msgpack nil.
    if kind == "enum":
        return 0
    if base == "bool":
        return False
    if base in _FLOAT_TYPES:
        return 0.0
    if base in _INT_TYPES:
        return 0
    if base == "DateTime":
        return DATETIME_MIN
    return None


def _encode(base, is_array, kind, nullable, v):
    if v is None:
        return None if nullable else _zero(base, kind)
    if is_array:
        return [_encode(base, False, kind, True, x) for x in v]
    if kind == "model":
        return to_wire(v)
    if kind == "enum":
        return int(v)
    if base == "DateTime":
        return iso_to_ts(v) if isinstance(v, str) else v
    return v


def to_wire(obj):
    if obj is None:
        return None
    if isinstance(obj, dict):  # Dictionary<K,V> -> msgpack map, values converted
        return {k: to_wire(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [to_wire(x) for x in obj]
    name = type(obj).__name__
    if name in KEYS:
        fields = KEYS[name]
        arr = [None] * ((max(f[0] for f in fields) + 1) if fields else 0)
        for key, fn, base, is_array, kind, nullable in fields:
            arr[key] = _encode(base, is_array, kind, nullable, getattr(obj, fn, None))
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
    if base == "DateTime" and isinstance(v, msgpack.Timestamp):
        return ts_to_iso(v)
    return v


def from_array(name, arr):
    if name is None or name not in KEYS or not isinstance(arr, (list, tuple)):
        return arr
    kwargs = {}
    for key, fn, base, is_array, kind, nullable in KEYS[name]:
        v = _decode(base, is_array, kind, arr[key] if key < len(arr) else None)
        if v is not None:  # nil/missing -> let the field default (default(T)) apply
            kwargs[fn] = v
    return getattr(models, name)(**kwargs)


def pack(value) -> bytes:
    return msgpack.packb(to_wire(value), **_PACK) or b""


_LZ4_BLOCK = 99  # ExtType(99, <msgpack int uncompressedLen><raw lz4 block>)
_LZ4_BLOCK_ARRAY = 98  # [ExtType(98, lens...), bin(block0), .. bin(blockN-1)]


def _lz4_decompress(block, size: int) -> bytes:
    return lz4.block.decompress(bytes(block), uncompressed_size=size)


def _is_lz4_block_array(obj) -> bool:
    return (
        isinstance(obj, (list, tuple))
        and len(obj) >= 2
        and isinstance(obj[0], msgpack.ExtType)
        and obj[0].code == _LZ4_BLOCK_ARRAY
        and all(isinstance(x, (bytes, bytearray)) for x in obj[1:])
    )


def _decompress(obj):
    """Undo MessagePack-CSharp's request compression (Lz4BlockArray / Lz4Block)."""
    if _is_lz4_block_array(obj):
        up = msgpack.Unpacker(raw=False, strict_map_key=False)
        up.feed(obj[0].data)
        lengths = list(up)
        if len(lengths) == 1 and isinstance(lengths[0], (list, tuple)):
            lengths = list(lengths[0])
        out = bytearray()
        for length, block in zip(lengths, obj[1:]):
            out += _lz4_decompress(block, length)
        return msgpack.unpackb(bytes(out), **_UNPACK)
    if isinstance(obj, msgpack.ExtType) and obj.code == _LZ4_BLOCK:
        up = msgpack.Unpacker(raw=False, strict_map_key=False)
        up.feed(obj.data)
        length = up.unpack()
        return msgpack.unpackb(
            _lz4_decompress(obj.data[up.tell() :], length), **_UNPACK
        )
    return obj


def unpack(data):
    return _decompress(msgpack.unpackb(data, **_UNPACK))


class MsgpackResponse(Response):
    media_type = "application/vnd.msgpack"


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
    """
    Most routes do not use this! I have not found any routes that use this.

    If a route is using this DOUBLE CHECK that it's supposed to!

    ``ParseWithoutCommonResponse`` requires common response BUT just ignores everything that isn't "result"

    ``ParseWithoutCommonResponse`` still requires common response format.
    """
    return MsgpackResponse(content=pack(result), headers=response_headers())


def fault(error_code: str, message: str = "", stack_trace: str = "") -> "models.Fault":
    return models.Fault(error_code=error_code, message=message, stack_trace=stack_trace)


def deleted(type_name: str, id: int) -> "models.DeletedDataObject":
    return models.DeletedDataObject(type_name=type_name, id_=id)


def union(key: int, value) -> list:
    # IDataObject[] / INotificationObject[] element: [discriminatorKey, packed value].
    # e.g. union(IDATA_OBJECT_KEY["Live"], live_model) for a `present` entry.
    return [key, to_wire(value)]


respond = common_response


@overload
async def read_request(request: Request) -> Any: ...
@overload
async def read_request(request: Request, model: Type[T]) -> Optional[T]: ...


async def read_request(request: Request, model: Optional[Union[Type[T], str]] = None):
    raw = await request.body()
    if not raw:
        return None
    try:
        decoded = unpack(raw)
    except Exception:
        return None
    if model is None:
        return decoded
    name = model if isinstance(model, str) else model.__name__
    try:
        return from_array(name, decoded)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors())
