"""Serve the local Addressables catalogs. Everything derives from the decompressed
``assets/<kind>/<platform>/catalog.json`` that ``download_asset_catalogs`` writes:

- ``.json.br`` -> brotli of that json (the client decompresses it by extension)
- ``.hash``    -> SpookyHash-128 of that json, little-endian, lowercase hex

Both carry a ``Content-MD5`` (base64 of md5) matching the official server. Results
are memoized since compression/hashing the 10-50 MB catalogs is not free.
"""

import base64
import hashlib
from pathlib import Path
from typing import Dict, Optional, Tuple

import brotli
import spookyhash

from helpers.config import config

ASSETS = Path(__file__).resolve().parent.parent / "assets"
# where bundle requests are redirected when local_assets is off (hardcoded on purpose)
OFFICIAL_ASSET_URL = "https://assets-e.wds-stellarium.com/production"

_br_cache: Dict[str, Tuple[bytes, str]] = {}
_hash_cache: Dict[str, Tuple[bytes, str]] = {}


def _catalog(kind: str, platform: str) -> Optional[bytes]:
    path = ASSETS / kind / platform.lower() / "catalog.json"
    return path.read_bytes() if path.is_file() else None


def _content_md5(body: bytes) -> str:
    return base64.b64encode(hashlib.md5(body).digest()).decode()


def catalog_br(kind: str, platform: str) -> Optional[Tuple[bytes, str]]:
    key = f"{kind}/{platform.lower()}"
    if key not in _br_cache:
        raw = _catalog(kind, platform)
        if raw is None:
            return None
        body = brotli.compress(raw, quality=5)
        _br_cache[key] = (body, _content_md5(body))
    return _br_cache[key]


def catalog_hash(kind: str, platform: str) -> Optional[Tuple[bytes, str]]:
    key = f"{kind}/{platform.lower()}"
    if key not in _hash_cache:
        raw = _catalog(kind, platform)
        if raw is None:
            return None
        body = spookyhash.hash128(raw).to_bytes(16, "little").hex().encode()
        _hash_cache[key] = (body, _content_md5(body))
    return _hash_cache[key]


def local_assets_enabled() -> bool:
    return bool(config["local_assets"])


def bundle(kind: str, platform: str, rel_path: str) -> Optional[Tuple[bytes, str]]:
    """A local asset bundle and its Content-MD5, or None if not downloaded. Not
    memoized -- there are tens of thousands of bundles."""
    path = (ASSETS / kind / platform.lower() / rel_path).resolve()
    root = (ASSETS / kind / platform.lower()).resolve()
    if root not in path.parents or not path.is_file():  # stay inside the asset dir
        return None
    body = path.read_bytes()
    return body, _content_md5(body)


def official_url(kind: str, platform: str, version: str, rel_path: str) -> str:
    return f"{OFFICIAL_ASSET_URL}/{kind}/{platform}/{version}/{rel_path}"
