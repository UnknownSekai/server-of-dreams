from __future__ import annotations

import ast
import json
import pathlib
import re
from typing import Any
from urllib.parse import urlsplit

import msgpack

try:
    import lz4.block  # type: ignore
except ImportError:  # pragma: no cover
    lz4 = None  # type: ignore

from mitmproxy import contentviews, ctx, http

try:
    import models as _MODELS  # type: ignore
    from models.keys import KEYS  # type: ignore
    from models.unions import IDATA_OBJECT, INOTIFICATION_OBJECT  # type: ignore
except Exception:  # pragma: no cover
    _MODELS = None  # type: ignore
    KEYS = {}  # type: ignore
    IDATA_OBJECT = {}  # type: ignore
    INOTIFICATION_OBJECT = {}  # type: ignore

API_HOST = "lb-api.wds-stellarium.com"
_ROUTES_DIR = pathlib.Path(__file__).resolve().parent / "routes"

_LZ4_BLOCK = 99  # ExtType(99, <int uncompressedLen><raw lz4 block>)
_LZ4_BLOCK_ARRAY = 98  # [ExtType(98, lens...), bin(block0), .. bin(blockN-1)]


def _is_lz4_block_array(obj: Any) -> bool:
    """A ``[Ext(98, lens...), bin, bin, ...]`` MessagePack-CSharp block array."""
    return (
        isinstance(obj, (list, tuple))
        and len(obj) >= 2
        and isinstance(obj[0], msgpack.ExtType)
        and obj[0].code == _LZ4_BLOCK_ARRAY
        and all(isinstance(x, (bytes, bytearray)) for x in obj[1:])
    )


def _lz4_decompress(block: bytes, uncompressed_size: int) -> bytes:
    if lz4 is None:
        raise RuntimeError("LZ4-compressed body but the 'lz4' package isn't installed")
    return lz4.block.decompress(bytes(block), uncompressed_size=uncompressed_size)


def _join_lz4_block_array(obj) -> bytes:
    """Decompress every block of a Lz4BlockArray and concatenate to raw bytes."""
    up = msgpack.Unpacker(raw=False, strict_map_key=False)
    up.feed(obj[0].data)  # the ext holds N concatenated (or array-wrapped) lengths
    lengths = list(up)
    if len(lengths) == 1 and isinstance(lengths[0], (list, tuple)):
        lengths = list(lengths[0])
    out = bytearray()
    for length, block in zip(lengths, obj[1:]):
        out += _lz4_decompress(block, length)
    return bytes(out)


def _decompress_lz4_block_ext(data: bytes) -> bytes:
    up = msgpack.Unpacker(raw=False, strict_map_key=False)
    up.feed(data)
    length = up.unpack()
    return _lz4_decompress(data[up.tell() :], length)


def _decompress_lz4(obj: Any) -> Any:
    if _is_lz4_block_array(obj):
        inner = [_decompress_lz4(x) for x in _unpack_all(_join_lz4_block_array(obj))]
        return inner[0] if len(inner) == 1 else inner
    if isinstance(obj, msgpack.ExtType) and obj.code == _LZ4_BLOCK:
        raw = _decompress_lz4_block_ext(obj.data)
        inner = [_decompress_lz4(x) for x in _unpack_all(raw)]
        return inner[0] if len(inner) == 1 else inner
    if isinstance(obj, list):
        return [_decompress_lz4(x) for x in obj]
    if isinstance(obj, tuple):
        return tuple(_decompress_lz4(x) for x in obj)
    if isinstance(obj, dict):
        return {k: _decompress_lz4(v) for k, v in obj.items()}
    return obj


def _decode_wds(data: bytes) -> list[Any]:
    return [_decompress_lz4(o) for o in _unpack_all(data)]


def _unhandled_lz4(obj: Any, _depth: int = 0) -> bool:
    """True only if an LZ4 ext survived :func:`_decompress_lz4` — a real gap.

    Deliberately says nothing about ``bin`` fields: models carry ordinary byte
    arrays, and guessing "long bin == compressed" made the view reject bodies
    it had already decoded correctly.
    """
    if _depth > 16:
        return False
    if isinstance(obj, msgpack.ExtType):
        return obj.code in (_LZ4_BLOCK, _LZ4_BLOCK_ARRAY)
    if isinstance(obj, (list, tuple)):
        return any(_unhandled_lz4(x, _depth + 1) for x in obj)
    if isinstance(obj, dict):
        return any(_unhandled_lz4(v, _depth + 1) for v in obj.values())
    return False


def _bin_repr(b: bytes, limit: int = 64) -> str:
    text = b[:limit].hex(" ")
    if len(b) > limit:
        text += " ..."
    return f"<bin {len(b)} bytes: {text}>"


def _json_default(o: Any) -> Any:
    if isinstance(o, (bytes, bytearray)):
        return _bin_repr(bytes(o))
    if isinstance(o, msgpack.ExtType):
        return {"_ext": o.code, "data": _bin_repr(o.data)}
    return str(o)


def _is_wds_api(flow) -> bool:
    if not isinstance(flow, http.HTTPFlow):
        return False
    host = getattr(ctx.options, "wds_host", API_HOST) or API_HOST
    return host in flow.request.pretty_host and "/api/" in flow.request.path


def _unpack_all(data: bytes) -> list[Any]:
    up = msgpack.Unpacker(raw=False, strict_map_key=False)
    up.feed(data)
    return list(up)


def _hexdump(data: bytes, limit: int = 2048) -> str:
    view = data[:limit]
    header = f"# {len(data)} bytes total"
    if len(data) > limit:
        header += f" (showing first {limit})"
    lines = [header]
    for off in range(0, len(view), 16):
        chunk = view[off : off + 16]
        hexs = " ".join(f"{b:02x}" for b in chunk)
        text = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        lines.append(f"{off:06x}  {hexs:<47}  {text}")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# route -> model resolution (built statically from routes/*.py) + field naming
# --------------------------------------------------------------------------- #
_RESPOND_FNS = {"respond", "common_response", "raw_response"}


def _const_str(node) -> str | None:
    return (
        node.value
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
        else None
    )


def _result_model(arg: ast.expr) -> tuple[str | None, bool]:
    is_array = False
    if isinstance(arg, (ast.List, ast.Tuple)) and len(arg.elts) == 1:
        arg, is_array = arg.elts[0], True
    if (
        isinstance(arg, ast.Call)
        and isinstance(arg.func, ast.Name)
        and arg.func.id[:1].isupper()
    ):
        return arg.func.id, is_array
    return None, False


def _build_route_map() -> dict[str, dict]:
    routes: dict[str, dict] = {}
    if not _ROUTES_DIR.is_dir():
        return routes
    for py in _ROUTES_DIR.glob("*.py"):
        if py.name == "__init__.py":
            continue
        try:
            tree = ast.parse(py.read_text(encoding="utf-8"))
        except Exception:
            continue
        prefix = ""
        for node in tree.body:
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
                for kw in node.value.keywords:
                    if kw.arg == "prefix":
                        prefix = _const_str(kw.value) or ""
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for dec in node.decorator_list:
                if not (
                    isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute)
                ):
                    continue
                if dec.func.attr not in ("post", "get", "put", "delete"):
                    continue
                sub = _const_str(dec.args[0]) if dec.args else None
                if sub is None:
                    continue
                op = next(
                    (_const_str(k.value) for k in dec.keywords if k.arg == "name"), None
                )
                info = {
                    "operation": op,
                    "request": None,
                    "result": None,
                    "result_is_array": False,
                    "raw": None,
                }
                for n in ast.walk(node):
                    if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Name)):
                        continue
                    if n.func.id == "read_request" and len(n.args) >= 2:
                        info["request"] = _const_str(n.args[1]) or info["request"]
                    elif (
                        n.func.id in _RESPOND_FNS and n.args and info["result"] is None
                    ):
                        model, is_array = _result_model(n.args[0])
                        if model:
                            info["result"] = model
                            info["result_is_array"] = is_array
                            info["raw"] = n.func.id == "raw_response"
                routes[prefix + sub] = info
    return routes


ROUTE_MAP: dict[str, dict] = _build_route_map()


def _template_to_regex(template: str) -> re.Pattern:
    """``/api/X/{id}/Y`` -> a regex matching ``/api/X/<anything>/Y``."""
    literals = re.split(r"\{[^{}]+\}", template)
    return re.compile("^" + "[^/]+".join(re.escape(p) for p in literals) + "$")


_ROUTE_PATTERNS: list[tuple[re.Pattern, dict]] = sorted(
    ((_template_to_regex(p), info) for p, info in ROUTE_MAP.items() if "{" in p),
    key=lambda it: it[0].pattern.count("/"),
    reverse=True,
)


def _route_info(path: str) -> dict:
    info = ROUTE_MAP.get(path)
    if info is not None:
        return info
    for pattern, info in _ROUTE_PATTERNS:
        if pattern.match(path):
            return info
    return {}


def _name_enum(enum_name: str, v: Any) -> Any:
    cls = getattr(_MODELS, enum_name, None) if _MODELS else None
    if cls is None or not isinstance(v, int):
        return v
    try:
        return cls(v).name
    except ValueError:
        return v  # value not defined in the enum — keep the raw int


def _fmt_datetime(v: Any) -> Any:
    to_datetime = getattr(v, "to_datetime", None)
    if to_datetime is None:
        return v
    try:
        return to_datetime().isoformat()
    except Exception:
        return v


def _name_field(kind: str, base: str, is_array: bool, v: Any) -> Any:
    if v is None:
        return None
    if is_array:
        return (
            [_name_field(kind, base, False, x) for x in v]
            if isinstance(v, (list, tuple))
            else v
        )
    if kind == "model":
        return _name_model(base, v)
    if kind == "enum":
        return _name_enum(base, v)
    if base == "DateTime":
        return _fmt_datetime(v)
    return v


def _name_model(model_name: str | None, arr: Any) -> Any:
    if not model_name or model_name not in KEYS or not isinstance(arr, (list, tuple)):
        return arr
    named: dict[str, Any] = {}
    for key, fn, base, is_array, kind, *_ in KEYS[model_name]:
        named[fn] = _name_field(
            kind, base, is_array, arr[key] if key < len(arr) else None
        )
    return named


def _name_result(model_name: str | None, value: Any, is_array: bool = False) -> Any:
    if not model_name or model_name not in KEYS or not isinstance(value, (list, tuple)):
        return value
    if not value:
        return value
    if is_array:
        return [_name_model(model_name, x) for x in value]
    fields = KEYS[model_name]
    slots = (max(f[0] for f in fields) + 1) if fields else 0
    if all(isinstance(x, (list, tuple)) and len(x) <= slots for x in value):
        return [_name_model(model_name, x) for x in value]
    return _name_model(model_name, value)


def _is_union_element(elem: Any, disc_map: dict) -> bool:
    return (
        isinstance(elem, (list, tuple))
        and len(elem) == 2
        and isinstance(elem[0], int)
        and elem[0] in disc_map
    )


def _name_union_list(value: Any, disc_map: dict) -> Any:
    if not isinstance(value, (list, tuple)):
        return value
    named = []
    for elem in value:
        if _is_union_element(elem, disc_map):
            model = disc_map[elem[0]]
            named.append({"_type": model, "value": _name_model(model, elem[1])})
        else:
            named.append(elem)
    return named


def _looks_like_idata_list(value: Any) -> bool:
    return (
        isinstance(value, (list, tuple))
        and bool(value)
        and all(_is_union_element(x, IDATA_OBJECT) for x in value)
    )


def _name_extras(extras: dict) -> dict:
    out: dict[str, Any] = {}
    if extras.get("faults"):
        out["faults"] = [_name_model("Fault", x) for x in extras["faults"]]
    if extras.get("present"):
        out["present"] = _name_union_list(extras["present"], IDATA_OBJECT)
    if extras.get("deleted"):
        out["deleted"] = [
            _name_model("DeletedDataObject", x) for x in extras["deleted"]
        ]
    if extras.get("notifications"):
        out["notifications"] = _name_union_list(
            extras["notifications"], INOTIFICATION_OBJECT
        )
    return out


def _split_envelope(objs: list[Any], raw: bool | None) -> tuple[Any, dict]:
    if raw is True:
        return (objs[0] if objs else None), {}
    if raw is False or len(objs) >= 2:
        extras = {
            "faults": objs[0] if len(objs) >= 1 else None,
            "present": objs[2] if len(objs) >= 3 else None,
            "deleted": objs[3] if len(objs) >= 4 else None,
            "notifications": objs[4] if len(objs) >= 5 else None,
        }
        return (objs[1] if len(objs) >= 2 else None), extras
    return (objs[0] if objs else None), {}


class WdsContentview(contentviews.Contentview):
    name = "WDS"
    syntax_highlight = "yaml"

    def prettify(self, data: bytes, metadata: contentviews.Metadata) -> str:
        flow = metadata.flow
        if not isinstance(flow, http.HTTPFlow):
            raise ValueError("not an HTTP flow")
        try:
            return self._decode(data, flow, metadata)
        except Exception as e:
            return (
                f"# WDS view could not decode this body: {type(e).__name__}: {e}\n"
                f"# Below is a lossless hex dump — copy it verbatim.\n\n"
                + _hexdump(data)
            )

    def _decode(
        self, data: bytes, flow: http.HTTPFlow, metadata: contentviews.Metadata
    ) -> str:
        path = urlsplit(flow.request.url).path
        info = _route_info(path)
        operation = info.get("operation") or f"{flow.request.method} {path}"

        objs = _decode_wds(data)
        if not objs:
            raise ValueError("empty MessagePack body")
        if metadata.http_message is flow.response:
            result, extras = _split_envelope(objs, info.get("raw"))
            model = info.get("result")
            if model:
                response = _name_result(
                    model, result, info.get("result_is_array", False)
                )
            elif _looks_like_idata_list(result):
                response = _name_union_list(result, IDATA_OBJECT)
            else:
                response = result
            out: dict[str, Any] = {"operation": operation, "response": response}
            out.update(_name_extras(extras))
        else:
            payload = objs[0] if objs else None
            out = {
                "operation": operation,
                "payload": _name_result(info.get("request"), payload),
            }

        if _unhandled_lz4(objs):
            out["_warning"] = (
                "an LZ4 ext survived decompression — some fields below are raw"
            )

        return json.dumps(out, ensure_ascii=False, indent=2, default=_json_default)

    def render_priority(self, data: bytes, metadata: contentviews.Metadata) -> float:
        if not data or not _is_wds_api(metadata.flow):
            return -1
        return 2


contentviews.add(WdsContentview())
