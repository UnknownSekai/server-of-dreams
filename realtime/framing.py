"""gRPC + MagicOnion framing for the realtime StreamingHubs.

Wire shape, both directions::

    gRPC:       flag(1 byte) + length(4 bytes big-endian) + payload
    MagicOnion: a MessagePack array inside the payload

The array's LENGTH is the message type -- there is no type byte on the wire for
the common cases. Shapes, verified against a live capture:

Client -> server
    ``[MessageId, MethodId, args]``   request that expects a response
    ``[MethodId, args]``              fire-and-forget request (no response)
    ``[0x7e, nil, nil, [ClientTime]]`` client heartbeat

Server -> client
    ``[MessageId, MethodId, result]``  response, echoing the request's MessageId
    ``[MessageId, status, detail, msg]`` response carrying an error
    ``[MethodId, args]``               broadcast (a receiver callback)
    ``[0x7f, nil, nil, nil]``          server heartbeat

A common trap: ``frame[0]`` on a REQUEST is the message id, not a message type.
Reading it as a type makes every request look like "RequestFireAndForget" and
shifts every argument by one.
"""

from __future__ import annotations

import io
import lz4.block
import msgpack

# MessagePack-CSharp extension types the game uses for compressed payloads.
_LZ4_BLOCK = 99  # ExtType(99, <msgpack int uncompressedLen><raw lz4 block>)
_LZ4_BLOCK_ARRAY = 98  # [ExtType(98, lens...), bin(block0), .. bin(blockN-1)]

# Heartbeat type bytes. These ARE explicit on the wire (position 0 of the array),
# unlike the request/response/broadcast shapes above.
TYPE_CLIENT_HEARTBEAT = 0x7E
TYPE_SERVER_HEARTBEAT = 0x7F

# gRPC frame flag: 0 = uncompressed, 1 = compressed.
FLAG_UNCOMPRESSED = 0
FLAG_COMPRESSED = 1

# The first message the server writes on every hub stream. It is a pure
# anti-buffering marker (so a reverse proxy flushes the response headers), NOT a
# protocol message: MagicOnion's client switch has no case for -1 and drops it.
# Kept byte-for-byte from MagicOnion.Server's `MarkerResponseBytes`.
MARKER_PAYLOAD = bytes([0x93, 0xFF, 0x00, 0x0C])  # msgpack: [-1, 0, nil]

_PACK = dict(use_bin_type=True)
_UNPACK = dict(raw=False, strict_map_key=False)


# --------------------------------------------------------------------------- #
# gRPC frame layer
# --------------------------------------------------------------------------- #
def split_grpc_frames(data: bytes) -> list[tuple[bool, bytes]]:
    """Split a gRPC body into ``(compressed, payload)`` pairs.

    A body of exactly zero bytes is a trailers-only reply, not an error. A body
    with a partial header is returned as-is so the caller can see the raw bytes
    instead of silently losing them.
    """
    out: list[tuple[bool, bytes]] = []
    off, n = 0, len(data)
    while off + 5 <= n:
        flag = data[off]
        length = int.from_bytes(data[off + 1 : off + 5], "big")
        start, end = off + 5, off + 5 + length
        if end > n:
            out.append((bool(flag), data[start:]))
            break
        out.append((bool(flag), data[start:end]))
        off = end
    return out


def wrap_grpc_frame(payload: bytes, compressed: bool = False) -> bytes:
    """Prefix a payload with the 5-byte gRPC frame header."""
    flag = FLAG_COMPRESSED if compressed else FLAG_UNCOMPRESSED
    return bytes([flag]) + len(payload).to_bytes(4, "big") + payload


# --------------------------------------------------------------------------- #
# Compression (MessagePack-CSharp Lz4BlockArray / Lz4Block)
# --------------------------------------------------------------------------- #
def _is_lz4_block_array(obj) -> bool:
    return (
        isinstance(obj, (list, tuple))
        and len(obj) >= 2
        and isinstance(obj[0], msgpack.ExtType)
        and obj[0].code == _LZ4_BLOCK_ARRAY
        and all(isinstance(x, (bytes, bytearray)) for x in obj[1:])
    )


def decompress(obj):
    """Undo MessagePack-CSharp's request compression, if present.

    Both extension types appear in real traffic, so a decoder that handles only
    one of them will drop payloads that look empty.
    """
    if _is_lz4_block_array(obj):
        up = msgpack.Unpacker(raw=False, strict_map_key=False)
        up.feed(obj[0].data)
        lengths = list(up)
        if len(lengths) == 1 and isinstance(lengths[0], (list, tuple)):
            lengths = list(lengths[0])
        out = bytearray()
        for length, block in zip(lengths, obj[1:]):
            out += lz4.block.decompress(bytes(block), uncompressed_size=length)
        return msgpack.unpackb(bytes(out), **_UNPACK)
    if isinstance(obj, msgpack.ExtType) and obj.code == _LZ4_BLOCK:
        up = msgpack.Unpacker(raw=False, strict_map_key=False)
        up.feed(obj.data)
        length = up.unpack()
        return msgpack.unpackb(
            lz4.block.decompress(obj.data[up.tell() :], uncompressed_size=length),
            **_UNPACK,
        )
    return obj


def _unwrap_ext(obj):
    """Turn a msgpack ``ExtType`` into something readable.

    Needed because ``unpack_payload`` is also used on frames that are NOT
    compressed as a whole -- ``JoinPrivateHallFromInviteAsync`` carries an
    ``ExtType(98)`` *inside* its arguments, and without this the caller sees an
    opaque ``ExtType(code=98, ...)`` and cannot tell it apart from a real payload.
    """
    if isinstance(obj, msgpack.ExtType):
        return {"__ext__": obj.code, "len": len(obj.data)}
    if isinstance(obj, list):
        return [_unwrap_ext(x) for x in obj]
    if isinstance(obj, tuple):
        return [_unwrap_ext(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _unwrap_ext(v) for k, v in obj.items()}
    return obj


def unpack_args(args):
    """Decompress a request's arguments if the client compressed them.

    A large argument list is sent as an ``[ExtType(98), block]`` array IN PLACE of the
    arguments, e.g. ``[MessageId, MethodId, [ExtType(98), b'...']]``. Without this the
    handler would see an opaque ext type instead of the real arguments -- which is
    exactly what happened to ``JoinPrivateHallFromInviteAsync`` before this existed.

    Order matters: the decompression check runs BEFORE anything flattens the ext type,
    because flattening turns the ExtType into a plain dict and the payload becomes
    unrecognisable. Ext types are deliberately NOT flattened here: the caller may still
    need to decompress them (a large response arrives the same way).
    """
    if _is_lz4_block_array(args):
        return decompress(args)
    if isinstance(args, msgpack.ExtType):
        return decompress(args)
    return args


def _decode_frame(payload: bytes):
    """MessagePack-decode a payload WITHOUT flattening ext types.

    ``read_message`` needs the raw ``ExtType`` objects because decompression depends on
    seeing them; flattening first would make a compressed argument list look like an
    ordinary array.
    """
    obj = msgpack.unpackb(payload, **_UNPACK)
    if isinstance(obj, list) and len(obj) == 1 and isinstance(obj[0], list):
        obj = obj[0]
    if _is_lz4_block_array(obj):
        return decompress(obj)
    if isinstance(obj, msgpack.ExtType) and obj.code == _LZ4_BLOCK:
        return decompress(obj)
    return obj


def unpack_payload(payload: bytes):
    """MessagePack-decode one gRPC payload into a human-readable object.

    For logging and tests: the result has no ``ExtType`` left, compressed frames are
    already expanded, and any remaining ext type is rendered as a small dict.
    """
    return _unwrap_ext(_decode_frame(payload))


def pack_payload(value) -> bytes:
    return msgpack.packb(value, **_PACK)


# --------------------------------------------------------------------------- #
# MagicOnion message layer
# --------------------------------------------------------------------------- #
class Message:
    """One decoded MagicOnion frame.

    ``kind`` is one of ``request``, ``fire_and_forget``, ``response``,
    ``broadcast``, ``heartbeat`` or ``unknown``.
    """

    __slots__ = ("kind", "message_id", "method_id", "args", "raw")

    def __init__(self, kind, message_id=None, method_id=None, args=None, raw=None):
        self.kind = kind
        self.message_id = message_id
        self.method_id = method_id
        self.args = args
        self.raw = raw

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return (
            f"Message(kind={self.kind!r}, message_id={self.message_id!r}, "
            f"method_id={self.method_id!r}, args={self.args!r})"
        )


def read_message(payload: bytes, direction: str = "c2s") -> Message:
    """Decode one payload into a :class:`Message`.

    ``direction`` decides how to read the first array element, because the SAME
    shape means different things per direction:

    * client -> server, 3 elements: ``[MessageId, MethodId, args]`` (a request)
    * server -> client, 3 elements: ``[MessageId, MethodId, result]`` (a response)
    * either, 2 elements: ``[MethodId, args]`` -- fire-and-forget outbound, or a
      broadcast (receiver callback) inbound. ``direction`` labels which.

    Reading a response as a request is harmless for naming, but it makes the log
    claim the server sent requests, so the distinction is kept.
    """
    obj = _decode_frame(payload)
    if not isinstance(obj, (list, tuple)) or not obj:
        return Message("unknown", raw=obj)

    head = obj[0]
    if head == TYPE_CLIENT_HEARTBEAT:
        return Message("heartbeat", raw=list(obj))
    if head == TYPE_SERVER_HEARTBEAT:
        return Message("heartbeat", raw=list(obj))

    two_element = "fire_and_forget" if direction == "c2s" else "broadcast"
    three_element = "request" if direction == "c2s" else "response"

    if len(obj) == 2:
        return Message(two_element, method_id=obj[0], args=unpack_args(obj[1]))
    if len(obj) == 3:
        return Message(
            three_element, message_id=obj[0], method_id=obj[1], args=unpack_args(obj[2])
        )
    if len(obj) >= 4:
        # A 4-element frame is an error response: [MessageId, status, detail, msg]
        return Message(
            "response_with_error",
            message_id=obj[0],
            method_id=obj[1],
            args=list(obj[2:]),
        )
    return Message("unknown", raw=list(obj))


def write_response(message_id: int, method_id: int, result) -> bytes:
    """Server -> client response to a request."""
    return pack_payload([message_id, method_id, result])


def write_error(
    message_id: int, status: int, detail: str = "", message: str = ""
) -> bytes:
    """Server -> client error response.

    Shape from MagicOnion's writer: Array(4) ``[MessageId, StatusCode, Detail,
    Message]``. ``status`` is a gRPC status code (12 = UNIMPLEMENTED,
    2 = UNKNOWN, 13 = INTERNAL).
    """
    return pack_payload([message_id, status, detail, message])


def write_broadcast(method_id: int, args) -> bytes:
    """Server -> client broadcast, i.e. a receiver callback.

    Array(2) ``[MethodId, SerializedArgument]`` -- note there is NO message id,
    which is exactly what makes a 2-element frame distinguishable from a
    response.
    """
    return pack_payload([method_id, args])


def write_client_heartbeat_response(client_time) -> bytes:
    """Reply to a client heartbeat.

    Array(5) ``[Type=0x7e, Nil, Nil, Nil, [ClientTime]]``.
    """
    return pack_payload([TYPE_CLIENT_HEARTBEAT, None, None, None, [client_time]])


def write_server_heartbeat() -> bytes:
    """Array(5) ``[Type=0x7f, Nil, Nil, Nil, Extras]``."""
    return pack_payload([TYPE_SERVER_HEARTBEAT, None, None, None, None])


def parse_client_heartbeat_time(msg: Message):
    """Pull the client timestamp out of a heartbeat frame, if present."""
    raw = msg.raw or []
    for item in raw:
        if isinstance(item, (list, tuple)) and item:
            return item[0]
    return None


def describe_message(msg: Message) -> str:
    if msg.kind == "request":
        return f"request msgId={msg.message_id} methodId={msg.method_id}"
    if msg.kind == "fire_and_forget":
        return f"fire-and-forget methodId={msg.method_id}"
    if msg.kind == "heartbeat":
        return "heartbeat"
    return f"unknown {msg.raw!r}"


__all__ = [
    "FLAG_COMPRESSED",
    "FLAG_UNCOMPRESSED",
    "MARKER_PAYLOAD",
    "Message",
    "TYPE_CLIENT_HEARTBEAT",
    "TYPE_SERVER_HEARTBEAT",
    "decompress",
    "describe_message",
    "pack_payload",
    "parse_client_heartbeat_time",
    "read_message",
    "split_grpc_frames",
    "unpack_payload",
    "wrap_grpc_frame",
    "write_broadcast",
    "write_client_heartbeat_response",
    "write_error",
    "write_response",
    "write_server_heartbeat",
]
