"""Read/write MasterMemory database blobs (the ``mastermemory_*.db`` master data).

Format: a MessagePack map ``tableName -> [offset, length]`` followed by a data
region of per-table blobs. Each blob is either a plain MessagePack array of rows
or a MessagePack-C# ``Lz4Block`` (ext type 99) wrapping ``[uncompressed_len]
[lz4-block bytes]``. A row is a MessagePack array of columns in ``[Key(n)]`` order.

``to_json``/``from_json`` make the rows JSON-safe by tagging the MessagePack types
that JSON can't hold (DateTime timestamps, byte arrays, extensions).
"""

import base64

import lz4.block
import msgpack

_LZ4_BLOCK = 99  # MessagePack-C# MessagePackCompression.Lz4Block ext code
_COMPRESS_MIN = 64  # only compress blobs at least this large


def unpack(db: bytes) -> dict:
    up = msgpack.Unpacker(raw=False, strict_map_key=False, use_list=True)
    up.feed(db)
    header = up.unpack()
    base = up.tell()
    tables = {}
    for name, (offset, length) in header.items():
        blob = db[base + offset : base + offset + length]
        obj = msgpack.unpackb(blob, raw=False, strict_map_key=False, use_list=True)
        if isinstance(obj, msgpack.ExtType) and obj.code == _LZ4_BLOCK:
            u = msgpack.Unpacker(raw=False)
            u.feed(obj.data)
            uncompressed_len = u.unpack()
            raw = lz4.block.decompress(
                obj.data[u.tell() :], uncompressed_size=uncompressed_len
            )
            obj = msgpack.unpackb(raw, raw=False, strict_map_key=False, use_list=True)
        tables[name] = obj
    return tables


def pack(tables: dict) -> bytes:
    header = {}
    parts = []
    offset = 0
    for name in sorted(tables):
        raw = msgpack.packb(tables[name], use_bin_type=True)
        if len(raw) >= _COMPRESS_MIN:
            payload = msgpack.packb(len(raw)) + lz4.block.compress(
                raw, store_size=False
            )
            blob = msgpack.packb(
                msgpack.ExtType(_LZ4_BLOCK, payload), use_bin_type=True
            )
        else:
            blob = raw
        header[name] = [offset, len(blob)]
        parts.append(blob)
        offset += len(blob)
    return msgpack.packb(header, use_bin_type=True) + b"".join(parts)


def to_json(obj):
    if isinstance(obj, msgpack.Timestamp):
        return {"__ts__": [obj.seconds, obj.nanoseconds]}
    if isinstance(obj, (bytes, bytearray)):
        return {"__bin__": base64.b64encode(obj).decode("ascii")}
    if isinstance(obj, msgpack.ExtType):
        return {"__ext__": obj.code, "d": base64.b64encode(obj.data).decode("ascii")}
    if isinstance(obj, list):
        return [to_json(x) for x in obj]
    if isinstance(obj, dict):
        return {k: to_json(v) for k, v in obj.items()}
    return obj


def from_json(obj):
    if isinstance(obj, dict):
        if "__ts__" in obj:
            seconds, nanoseconds = obj["__ts__"]
            return msgpack.Timestamp(seconds, nanoseconds)
        if "__bin__" in obj:
            return base64.b64decode(obj["__bin__"])
        if "__ext__" in obj:
            return msgpack.ExtType(obj["__ext__"], base64.b64decode(obj["d"]))
        return {k: from_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [from_json(x) for x in obj]
    return obj
