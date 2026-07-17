"""Helpers to turn raw WDS API bodies into human-readable, named structures.

Used by the mitmproxy addon and any traffic-inspection tooling. Given an
operation and a decoded MessagePack value, :func:`name_fields` recursively maps
the integer-keyed ``[Key(n)]`` arrays back to their field names using the models
in ``models_generated`` (so ``["JWT", 2, null]`` becomes
``{"token": "JWT", "ban_level": "Warning", "warned_until": null}``).
"""

from __future__ import annotations

from typing import Any, Optional

from . import routes
from .models import ENUM_REGISTRY, MODEL_REGISTRY

# (method, path) and query keys let us resolve a live URL to its operation.
_BY_PATH: dict[str, list[dict]] = {}
for _r in routes.ROUTES:
    _BY_PATH.setdefault(_r["path"], []).append(_r)


def operation_for(
    path: str, method: str, query_keys: Optional[list[str]] = None
) -> Optional[dict]:
    """Resolve a request path+method (and its query keys) to a ROUTES entry."""
    cands = _BY_PATH.get(
        path.rstrip("/") if path != "/api/Lessons/" else path
    ) or _BY_PATH.get(path)
    if not cands:
        # try with/without trailing slash
        cands = _BY_PATH.get(path.rstrip("/")) or _BY_PATH.get(path + "/")
    if not cands:
        return None
    method = method.upper()
    same_verb = [c for c in cands if c["method"] == method] or cands
    if len(same_verb) == 1:
        return same_verb[0]
    # disambiguate by query keys (e.g. /api/Circles vs /api/Circles?circleId=)
    qk = set(k.lower() for k in (query_keys or []))
    for c in same_verb:
        if set(k.lower() for k in c["query_keys"]) == qk:
            return c
    # prefer the one whose query keys are all present
    for c in same_verb:
        if c["query_keys"] and qk and set(k.lower() for k in c["query_keys"]) <= qk:
            return c
    return same_verb[0]


def name_fields(type_name: Optional[str], value: Any) -> Any:
    """Recursively name a decoded MessagePack value using a model's ``_FIELDS``.

    ``type_name`` is a model class name (``"AuthenticateResult"``) or None. Enum
    values are rendered as ``"Name (n)"``; arrays and nested models recurse.
    """
    if value is None or type_name is None:
        return value
    if type_name in ENUM_REGISTRY:
        try:
            return f"{ENUM_REGISTRY[type_name](value).name} ({value})"
        except ValueError:
            return value
    cls = MODEL_REGISTRY.get(type_name)
    if cls is None or not isinstance(value, (list, tuple)):
        return value
    out: dict[str, Any] = {}
    for key, py_name, base, is_array, kind in cls._FIELDS:  # type: ignore[attr-defined]
        v = value[key] if key < len(value) else None
        inner = base if kind in ("model", "enum") else None
        if is_array and isinstance(v, (list, tuple)):
            out[py_name] = [name_fields(inner, x) for x in v]
        else:
            out[py_name] = name_fields(inner, v)
    return out


def describe_request(path: str, method: str, query: dict, payload: Any) -> dict:
    """Full human-readable description of a request."""
    route = operation_for(path, method, list(query or {}))
    op = route["operation"] if route else None
    body = None
    if route and op and payload is not None:
        # the body is the op's single model/array param, if any
        params = route["params"]
        body_param = next(
            (
                p
                for p in params
                if p["type"].endswith("[]")
                or p["type"].split("<")[0].rstrip("[]") in MODEL_REGISTRY
            ),
            None,
        )
        if body_param:
            base = (
                body_param["type"][:-2]
                if body_param["type"].endswith("[]")
                else body_param["type"]
            )
            base = base.split("<")[0].split(".")[-1]
            if body_param["type"].endswith("[]") and isinstance(payload, (list, tuple)):
                body = [name_fields(base, x) for x in payload]
            else:
                body = name_fields(base, payload)
        else:
            body = payload
    else:
        body = payload
    return {
        "operation": op,
        "method": method,
        "path": path,
        "query": query or {},
        "result_type": route["result"] if route else None,
        "payload": body,
    }


def describe_response(path: str, method: str, query: dict, decoded: Any) -> dict:
    route = operation_for(path, method, list(query or {}))
    op = route["operation"] if route else None
    named = decoded
    if route and route.get("result_model"):
        if route["result_is_array"] and isinstance(decoded, (list, tuple)):
            named = [name_fields(route["result_model"], x) for x in decoded]
        else:
            named = name_fields(route["result_model"], decoded)
    return {
        "operation": op,
        "result_type": route["result"] if route else None,
        "response": named,
    }
