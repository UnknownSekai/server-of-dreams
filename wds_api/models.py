"""Wire constants + MessagePack model base with recursive array decoding.

MessagePack contract
--------------------
Every request/response DTO in ``Sirius.Entity`` is a ``[MessagePackObject]``
with integer ``[Key(n)]`` attributes, so it serializes as a **MessagePack array
in key order** (NOT a map). ``models_generated.py`` holds the 263 DTOs + 69
enums extracted from the binary; each carries a ``_FIELDS`` descriptor that this
base uses to decode/encode nested models and enums recursively.

    res = api.account_authenticate(AuthenticatePayload(login_token="...")).response
    # res is already an AuthenticateResult when a result model is known
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any, Dict, Generic, Optional, Type, TypeVar

T = TypeVar("T")

# populated by models_generated at import time
MODEL_REGISTRY: Dict[str, type] = {}
ENUM_REGISTRY: Dict[str, type] = {}


class Headers:
    # request
    CLIENT_VERSION = "X-Client-Version"
    ASSET_VERSION = "X-Assets-Version"
    # response
    DATE = "date"
    TIMEWARP_DATE = "x-timewarp-date"
    SERVER_VERSION = "X-Server-Version"
    MAINTENANCE = "X-Maintenance"
    MAINTENANCE_MESSAGE = "X-Maintenance-Message"
    TOKEN_EXPIRED = "X-Token-Expired"
    MASTERDATA_VERSION = "X-MasterData-Version"
    MASTERDATA_URI = "X-MasterData-Uri"
    MASTERDATA_SAS_TOKEN = "X-MasterData-SasToken"
    MASTERDATA_PUBLISH_TIMESTAMP = "X-MasterData-PublishTimestamp"
    FEATURE_MAINTENANCE = "X-FM"


@dataclass
class ApiActionResult(Generic[T]):
    """Mirror of ``Sirius.Api.ApiActionResult<T>``."""

    status: int
    response: Optional[T] = None
    error_message: str = ""
    is_http_error: bool = False
    is_network_error: bool = False
    is_cancel: bool = False
    is_critical: bool = False

    @property
    def is_ok(self) -> bool:
        return not self.is_error

    @property
    def is_error(self) -> bool:
        return self.is_http_error or self.is_network_error or self.is_cancel


def _decode(base_type: str, is_array: bool, kind: str, value: Any) -> Any:
    if value is None:
        return None
    if is_array:
        return [_decode(base_type, False, kind, v) for v in value]
    if kind == "model":
        cls = MODEL_REGISTRY.get(base_type)
        if cls is not None and isinstance(value, (list, tuple)):
            return cls.from_array(value)
        return value
    if kind == "enum":
        enum = ENUM_REGISTRY.get(base_type)
        try:
            return enum(value) if enum is not None else value
        except ValueError:
            return value
    return value


def _encode(value: Any) -> Any:
    if isinstance(value, MsgpackModel):
        return value.to_array()
    if isinstance(value, (list, tuple)):
        return [_encode(v) for v in value]
    # IntEnum serializes as its int value automatically via msgpack
    return value


class MsgpackModel:
    """Base for ``[Key(n)]`` array-serialized DTOs.

    Generated subclasses declare
    ``_FIELDS = ((key, py_name, base_type, is_array, kind), ...)`` where ``key`` is
    the MessagePack ``[Key(n)]`` index (the array position — may have gaps, and
    includes merged base-class keys) and ``kind`` is ``"prim"``/``"enum"``/``"model"``.
    """

    _FIELDS: tuple = ()

    def to_array(self) -> list:
        if not self._FIELDS:
            return []
        size = max(spec[0] for spec in self._FIELDS) + 1
        arr: list = [None] * size
        for key, name, _bt, _arr, _kind in self._FIELDS:
            arr[key] = _encode(getattr(self, name))
        return arr

    @classmethod
    def from_array(cls: Type[T], arr) -> T:
        if not isinstance(arr, (list, tuple)):
            # a scalar / already-decoded value
            return arr  # type: ignore[return-value]
        obj = cls()  # type: ignore[call-arg]
        for key, name, base_type, is_array, kind in cls._FIELDS:  # type: ignore[attr-defined]
            val = arr[key] if key < len(arr) else None
            setattr(obj, name, _decode(base_type, is_array, kind, val))
        return obj
