"""Talk to the official WDS API so download scripts discover the *current* asset /
master-data versions instead of hardcoding a value that goes stale on every update.

    from scripts._sirius import environment, master_data_manifest
    env = environment()               # EnvironmentResult (asset_version, urls, ...)  -- no auth
    manifest = master_data_manifest() # registers+authenticates, then the manifest (uri, sas, ...)

The Authenticate ApkHash / signature / app version are the constants of the official
2.31.0.489 client (from an Account/Authenticate capture).
"""

import lz4.block
import msgpack
import requests

from helpers.msgpack import from_array, to_wire
from models import AuthenticatePayload, RegisterPayload

_LZ4_BLOCK = 99
_LZ4_BLOCK_ARRAY = 98


class MaintenanceError(Exception):
    """Raised when the official server signals maintenance (X-Maintenance header)."""


OFFICIAL = "https://lb-api.wds-stellarium.com"

_CLIENT_VERSION = "2.31.0"
_APP_VERSION = "2.31.0.489"
_GAME_VERSION = 2  # GameVersions.GooglePlay
_APK_HASH = "E75761F189DDC378894B8DD770B129057F242148:1EFF46A116B8A6B91E858B34D722C18B54F64132:8D695CF32507DD218633ABAF429370A259519AEA"
_APK_SIGNATURE = "762B0A9B72279219081CAA00F83AA8CEEACED4B8A750DAF70B4F46CFBC4C6D1C"


def _request(
    path, method="POST", payload=None, token="", query=None
) -> requests.Response:
    headers = {
        "X-Client-Version": _CLIENT_VERSION,
        "X-Platform": "Android",
        "Accept": "application/vnd.msgpack",
    }
    if token:
        headers["Authorization"] = token
    body = None
    if payload is not None:
        body = msgpack.packb(to_wire(payload), use_bin_type=True) or b""
        headers["Content-Type"] = "application/vnd.msgpack"
    resp = requests.request(
        method, OFFICIAL + path, params=query, data=body, headers=headers, timeout=60
    )
    maintenance = resp.headers.get("X-Maintenance", "").strip().lower()
    if maintenance not in ("", "0", "false"):
        raise MaintenanceError(resp.headers.get("X-Maintenance-Message", ""))
    resp.raise_for_status()
    return resp


def _unpack_all(data: bytes) -> list:
    up = msgpack.Unpacker(raw=False, strict_map_key=False)
    up.feed(data)
    return list(up)


def _is_block_array(obj) -> bool:
    return (
        isinstance(obj, (list, tuple))
        and len(obj) >= 2
        and isinstance(obj[0], msgpack.ExtType)
        and obj[0].code == _LZ4_BLOCK_ARRAY
        and all(isinstance(x, (bytes, bytearray)) for x in obj[1:])
    )


def _decompress(obj):
    # official responses are MessagePack-CSharp Lz4-compressed (block-array/ext-99)
    if _is_block_array(obj):
        lengths = _unpack_all(obj[0].data)
        if len(lengths) == 1 and isinstance(lengths[0], (list, tuple)):
            lengths = list(lengths[0])
        out = bytearray()
        for length, block in zip(lengths, obj[1:]):
            out += lz4.block.decompress(bytes(block), uncompressed_size=length)
        inner = [_decompress(x) for x in _unpack_all(bytes(out))]
        return inner[0] if len(inner) == 1 else inner
    if isinstance(obj, msgpack.ExtType) and obj.code == _LZ4_BLOCK:
        up = msgpack.Unpacker(raw=False)
        up.feed(obj.data)
        length = up.unpack()
        raw = lz4.block.decompress(obj.data[up.tell() :], uncompressed_size=length)
        inner = [_decompress(x) for x in _unpack_all(raw)]
        return inner[0] if len(inner) == 1 else inner
    if isinstance(obj, list):
        return [_decompress(x) for x in obj]
    return obj


def _result(resp: requests.Response, model_name: str):
    # common-response envelope: [faults, result, present, deleted, notifications]
    objs = [_decompress(o) for o in _unpack_all(resp.content)]
    result = objs[1] if len(objs) >= 2 else (objs[0] if objs else None)
    return from_array(model_name, result)


def environment():
    """The current EnvironmentResult (asset_version, asset_url, ...) -- no auth needed."""
    resp = _request(
        "/api/Environment",
        query={"applicationVersion": _CLIENT_VERSION, "gameVersion": _GAME_VERSION},
    )
    return _result(resp, "EnvironmentResult")


def _session_token() -> str:
    reg = _result(
        _request(
            "/api/Account/Register", payload=RegisterPayload(name="server-of-dreams")
        ),
        "AccountRegistResult",
    )
    auth = _result(
        _request(
            "/api/Account/Authenticate",
            payload=AuthenticatePayload(
                login_token=reg.token,
                game_version=_GAME_VERSION,
                apk_hash=_APK_HASH,
                apk_application_signature=_APK_SIGNATURE,
                application_version=_APP_VERSION,
            ),
        ),
        "AuthenticateResult",
    )
    return auth.token


def master_data_manifest():
    """Register + authenticate a throwaway account, then return the current MasterDataManifest."""
    return _result(
        _request("/api/data/master", method="GET", token=_session_token()),
        "MasterDataManifest",
    )
