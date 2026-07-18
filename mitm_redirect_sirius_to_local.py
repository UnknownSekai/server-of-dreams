"""Redirect the official game API to the local emulator.

Run the game through mitmproxy with this addon loaded and every
``https://lb-api.wds-stellarium.com/api/...`` call is answered by the FastAPI app
in this repo instead of the live server. Everything else the client fetches
(asset bundles, the master-data blob on Azure, ...) is left alone and still goes
out to the real hosts.

    mitmproxy -s mitm_redirect_sirius_to_local.py
    mitmproxy -s mitm_redirect_sirius_to_local.py -s mitmweb_helper.py   # + WDS view

Options (``--set name=value``):

    sod_local        base URL of the emulator      (default: from config.yml)
    sod_host         official host to intercept    (lb-api.wds-stellarium.com)
    sod_prefix       only paths under this prefix  (/api/)
    sod_fallback     unimplemented route -> real server   (true)
    sod_passthrough  substrings always sent to the real server (repeatable)
    sod_keep_host    keep the original Host header on the local call (true)

How it works: rather than rewriting the request's destination, the addon calls
the emulator itself and installs the result as the flow's response. The flow
keeps the original ``lb-api...`` host, so the ``WDS`` contentview in
``mitmweb_helper.py`` still recognises and decodes it, and declining to set a
response is all it takes to let a request fall through to the real server.
"""

from __future__ import annotations

import pathlib
from typing import Optional, Sequence
from urllib.parse import urlsplit, urlunsplit

import httpx
import msgpack
from mitmproxy import ctx, http

API_HOST = "lb-api.wds-stellarium.com"
DEFAULT_LOCAL = "http://127.0.0.1:8002"

# Set per-hop by the proxy; forwarding them to the emulator is wrong.
_HOP_BY_HOP = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
}
# httpx hands back a decoded body, so the encoding/length of the *encoded* one
# must not survive onto the response we hand the client.
_DROP_FROM_RESPONSE = _HOP_BY_HOP | {"content-encoding", "content-length"}

# Fault codes the emulator emits for a route it doesn't serve. app.py turns
# HTTPException into a common_response, which defaults to HTTP 200 — so
# "route missing" arrives as 200 + a fault, not as a 404.
_UNIMPLEMENTED_CODES = {"404", "405"}


def _local_from_config() -> str:
    """``http://host:port`` from config.yml, falling back to the default."""
    try:
        import yaml

        cfg = (
            yaml.safe_load(
                (pathlib.Path(__file__).resolve().parent / "config.yml").read_text(
                    encoding="utf-8"
                )
            )
            or {}
        )
    except Exception:
        return DEFAULT_LOCAL
    host = str(cfg.get("host") or "127.0.0.1")
    if host in ("0.0.0.0", "::"):  # a bind address, not something to connect to
        host = "127.0.0.1"
    return f"http://{host}:{int(cfg.get('port') or 8002)}"


def _first_fault_code(body: bytes) -> Optional[str]:
    """Error code of the first fault in a common-response envelope, if any.

    The envelope is five concatenated msgpack objects, the first being
    ``Fault[]`` — each fault an array whose slot 0 is the error code.
    """
    try:
        up = msgpack.Unpacker(raw=False, strict_map_key=False)
        up.feed(body)
        faults = up.unpack()
    except Exception:
        return None
    if not isinstance(faults, (list, tuple)) or not faults:
        return None
    first = faults[0]
    if isinstance(first, (list, tuple)) and first and isinstance(first[0], str):
        return first[0]
    return None


class RedirectToLocal:
    def load(self, loader):
        loader.add_option(
            "sod_local", str, _local_from_config(), "base URL of the local emulator"
        )
        loader.add_option("sod_host", str, API_HOST, "official API host to intercept")
        loader.add_option("sod_prefix", str, "/api/", "only redirect paths under this")
        loader.add_option(
            "sod_fallback",
            bool,
            True,
            "send routes the emulator doesn't implement to the real server",
        )
        loader.add_option(
            "sod_passthrough",
            Sequence[str],
            [],
            "path substrings to always send to the real server",
        )
        loader.add_option(
            "sod_keep_host",
            bool,
            True,
            "keep the original Host header on the local call",
        )
        # trust_env=False matters: with HTTP(S)_PROXY set — likely, since a proxy
        # is running — httpx would route the emulator call back through mitmproxy.
        self.client = httpx.AsyncClient(
            trust_env=False, follow_redirects=False, timeout=30.0
        )

    async def done(self):
        await self.client.aclose()

    # -- routing decisions ---------------------------------------------------
    def _target(self, flow: http.HTTPFlow) -> Optional[str]:
        """The emulator URL for this flow, or None to leave it to the real server."""
        if ctx.options.sod_host not in flow.request.pretty_host:
            return None
        path = urlsplit(flow.request.url).path
        if not path.startswith(ctx.options.sod_prefix):
            return None
        if any(frag and frag in path for frag in ctx.options.sod_passthrough):
            ctx.log.info(f"[sod] passthrough {path}")
            return None
        local = urlsplit(ctx.options.sod_local.rstrip("/"))
        original = urlsplit(flow.request.url)
        return urlunsplit(
            (local.scheme, local.netloc, original.path, original.query, "")
        )

    def _is_unimplemented(self, resp: httpx.Response) -> bool:
        if resp.status_code in (404, 405):
            return True
        return _first_fault_code(resp.content) in _UNIMPLEMENTED_CODES

    # -- the hook ------------------------------------------------------------
    async def request(self, flow: http.HTTPFlow) -> None:
        if flow.response is not None:  # already answered by another addon
            return
        url = self._target(flow)
        if url is None:
            return

        headers = {
            k: v
            for k, v in flow.request.headers.items()
            if k.lower() not in _HOP_BY_HOP
        }
        if not ctx.options.sod_keep_host:
            headers.pop("Host", None)

        path = urlsplit(flow.request.url).path
        try:
            resp = await self.client.request(
                flow.request.method,
                url,
                headers=headers,
                content=flow.request.raw_content or b"",
            )
        except httpx.RequestError as exc:
            reason = f"{type(exc).__name__}: {exc}"
            if ctx.options.sod_fallback:
                ctx.log.warn(f"[sod] emulator unreachable ({reason}) -> real server")
                return
            flow.response = http.Response.make(
                502,
                f"emulator unreachable: {reason}".encode(),
                {"Content-Type": "text/plain"},
            )
            return

        if ctx.options.sod_fallback and self._is_unimplemented(resp):
            ctx.log.warn(f"[sod] {path} not implemented locally -> real server")
            return

        flow.response = http.Response.make(
            resp.status_code,
            resp.content,
            [
                (k.encode(), v.encode())
                for k, v in resp.headers.multi_items()
                if k.lower() not in _DROP_FROM_RESPONSE
            ],
        )
        ctx.log.info(f"[sod] {flow.request.method} {path} -> local {resp.status_code}")


addons = [RedirectToLocal()]
