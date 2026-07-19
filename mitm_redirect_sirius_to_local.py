"""Redirect the official game API + assets to the local emulator.

mitmproxy -s mitm_redirect_sirius_to_local.py
mitmproxy -s mitm_redirect_sirius_to_local.py -s mitmweb_helper.py
"""

from __future__ import annotations

from urllib.parse import urlsplit, urlunsplit

import httpx
from mitmproxy import http

LOCAL = "http://127.0.0.1:20000"
API_HOST = "lb-api.wds-stellarium.com"
ASSET_HOST = "assets-e.wds-stellarium.com"
REALTIME_HOST = "lb-realtime.wds-stellarium.com"

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
_DROP_FROM_RESPONSE = _HOP_BY_HOP | {"content-encoding", "content-length"}


class RedirectToLocal:
    def __init__(self):
        # trust_env=False bypasses the running proxy (no loop); follow_redirects so a bundle
        # the emulator redirects to the official CDN is fetched directly and served here.
        self.client = httpx.AsyncClient(
            trust_env=False, follow_redirects=True, timeout=30.0
        )

    async def done(self):
        await self.client.aclose()

    def _target(self, flow: http.HTTPFlow):
        host = flow.request.pretty_host
        parts = urlsplit(flow.request.url)
        if API_HOST in host and not parts.path.startswith("/api/"):
            return None
        if API_HOST not in host and ASSET_HOST not in host:
            return None
        local = urlsplit(LOCAL)
        return urlunsplit((local.scheme, local.netloc, parts.path, parts.query, ""))

    async def request(self, flow: http.HTTPFlow) -> None:
        if flow.response is not None:
            return
        url = self._target(flow)
        if url is None:
            return
        headers = {
            k: v
            for k, v in flow.request.headers.items()
            if k.lower() not in _HOP_BY_HOP
        }
        try:
            resp = await self.client.request(
                flow.request.method,
                url,
                headers=headers,
                content=flow.request.raw_content or b"",
            )
        except httpx.RequestError as exc:
            flow.response = http.Response.make(
                502,
                f"emulator unreachable: {exc}".encode(),
                {"Content-Type": "text/plain"},
            )
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


addons = [RedirectToLocal()]
