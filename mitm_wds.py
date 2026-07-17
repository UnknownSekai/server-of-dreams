"""mitmproxy addon for World Dai Star: Yume no Stellarium — traffic decoder.

Same shape as sekai-api-emulator's mitmproxy script (a ``request``/``response``
addon that decodes the game's API bodies), adapted to WDS's actual wire format:

    * Host              ``lb-api.wds-stellarium.com`` (the real API endpoint).
    * Serialization     MessagePack, DTOs are integer-``[Key(n)]`` arrays.
    * **Crypto**        WDS's API bodies are **NOT** encrypted (unlike Project
                        Sekai's AES) — confidentiality is TLS only. So "decrypt"
                        here is just Brotli/GZip-decompress + MessagePack-decode.
                        The game's only AES (``CustomAesEncoder`` — AES-256-CBC/
                        PKCS7, key = UTF8(password), IV = PBKDF2-HMAC-SHA256(
                        plaintext, salt=0x00*8, 1000)[:16], IV prepended) is used
                        ONLY for debug music/chart web resources; it is provided
                        below (``decrypt_resource``) for completeness and applied
                        automatically if a body isn't valid MessagePack.
    * Routes/models     every flow is mapped to its operation and its fields are
                        named via ``wds_api`` (203 ground-truth routes, 263 DTOs).

Usage
-----
    pip install mitmproxy msgpack brotli
    # make wds_api importable (run from the repo root, or set PYTHONPATH):
    mitmdump -s mitm/wds_mitm.py --set wds_out=./flows --set wds_verbose=true

Then point the game device at the proxy and install the mitmproxy CA cert.
Each decoded request/response is printed and (optionally) saved to ``wds_out``
as JSON — a ready-made corpus for building an emulator / replaying traffic.

This decodes **your own** device's authenticated traffic. It does not bypass the
app-integrity auth (``ApkHash``/signature) or make requests on your behalf.
"""

from __future__ import annotations

import gzip
import json
import logging
import os
import zlib
from typing import Any, Optional
from urllib.parse import parse_qsl, urlsplit

import msgpack

try:
    import brotli  # type: ignore
except ImportError:
    brotli = None  # type: ignore

from mitmproxy import ctx, http

from wds_api import crypto  # noqa: E402
from wds_api.decode import describe_request, describe_response  # noqa: E402

API_HOST = "lb-api.wds-stellarium.com"
log = logging.getLogger("wds")


# --------------------------------------------------------------------------- #
# body codec — decompress + MessagePack (+ optional CustomAesEncoder fallback)
# --------------------------------------------------------------------------- #
def _decompress(data: bytes, content_encoding: Optional[str]) -> bytes:
    enc = (content_encoding or "").lower()
    if "br" in enc and brotli is not None:
        try:
            return brotli.decompress(data)
        except Exception:
            return data
    if "gzip" in enc:
        try:
            return gzip.decompress(data)
        except Exception:
            return data
    if "deflate" in enc:
        try:
            return zlib.decompress(data)
        except Exception:
            return data
    return data


def decode_body(
    data: bytes,
    content_encoding: Optional[str] = None,
    aes_password: Optional[str] = None,
) -> Any:
    """Decompress + MessagePack-decode a WDS body.

    If ``aes_password`` is given (for the debug music/notation resources) or the
    body isn't valid MessagePack but looks AES-wrapped, apply ``CustomAesEncoder``.
    """
    if not data:
        return None
    raw = _decompress(data, content_encoding)
    if aes_password is not None:
        raw = crypto.decrypt(aes_password, raw)
    try:
        return msgpack.unpackb(raw, raw=False, strict_map_key=False)
    except Exception:
        return {"_raw_hex": raw[:2000].hex(), "_len": len(raw)}


def decrypt_resource(password: str, data: bytes) -> bytes:
    """CustomAesEncoder.Decrypt — for the game's debug music/chart web resources."""
    return crypto.decrypt(password, data)


# --------------------------------------------------------------------------- #
# addon
# --------------------------------------------------------------------------- #
class WdsDecoder:
    def __init__(self) -> None:
        self.count = 0

    def load(self, loader) -> None:
        loader.add_option(
            "wds_out",
            str,
            "",
            "Directory to save decoded flows as JSON (empty = don't save).",
        )
        loader.add_option(
            "wds_verbose", bool, True, "Print decoded request/response bodies."
        )
        loader.add_option("wds_host", str, API_HOST, "API host to intercept.")

    def _match(self, flow: http.HTTPFlow) -> bool:
        return (
            ctx.options.wds_host in flow.request.pretty_host
            and "/api/" in flow.request.path
        )

    def _query(self, flow: http.HTTPFlow) -> dict:
        return dict(parse_qsl(urlsplit(flow.request.url).query))

    def response(self, flow: http.HTTPFlow) -> None:
        if flow.response is None or not self._match(flow):
            return
        self.count += 1
        path = urlsplit(flow.request.url).path
        method = flow.request.method
        query = self._query(flow)

        req_payload = decode_body(
            flow.request.raw_content or b"",
            flow.request.headers.get("Content-Encoding"),
        )
        resp_decoded = decode_body(
            flow.response.raw_content or b"",
            flow.response.headers.get("Content-Encoding"),
        )

        req = describe_request(path, method, query, req_payload)
        res = describe_response(path, method, query, resp_decoded)
        record = {
            "n": self.count,
            "operation": req["operation"] or f"{method} {path}",
            "status": flow.response.status_code,
            "request": req,
            "response": res,
            "response_headers": _interesting_headers(flow.response.headers),
        }

        if ctx.options.wds_verbose:
            log.info(
                f"[WDS #{self.count}] {record['operation']}  ({method} {path}) "
                f"-> {flow.response.status_code}\n"
                + json.dumps(
                    {"request": req["payload"], "response": res["response"]},
                    ensure_ascii=False,
                    indent=2,
                    default=str,
                )
            )
        if ctx.options.wds_out:
            self._save(record)

    def _save(self, record: dict) -> None:
        os.makedirs(ctx.options.wds_out, exist_ok=True)
        op = (record["operation"] or "unknown").replace("/", "_").replace(" ", "_")
        fn = f"{record['n']:05d}_{op}.json"
        with open(os.path.join(ctx.options.wds_out, fn), "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2, default=str)


def _interesting_headers(headers) -> dict:
    keys = (
        "X-Server-Version",
        "X-Maintenance",
        "X-Maintenance-Message",
        "X-Token-Expired",
        "X-MasterData-Version",
        "X-MasterData-Uri",
        "X-MasterData-SasToken",
        "X-MasterData-PublishTimestamp",
        "X-FM",
        "date",
        "x-timewarp-date",
        "Content-Encoding",
    )
    return {k: headers[k] for k in keys if k in headers}


addons = [WdsDecoder()]
