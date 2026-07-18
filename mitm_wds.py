import gzip
import json
import logging
import os
import zlib
from urllib.parse import urlsplit

import msgpack
from mitmproxy import ctx, http

try:
    import brotli
except ImportError:
    brotli = None

log = logging.getLogger("wds")


def decode(data, encoding):
    if not data:
        return None
    enc = (encoding or "").lower()
    try:
        if "br" in enc and brotli:
            data = brotli.decompress(data)
        elif "gzip" in enc:
            data = gzip.decompress(data)
        elif "deflate" in enc:
            data = zlib.decompress(data)
    except Exception:
        pass
    try:
        return msgpack.unpackb(data, raw=False, strict_map_key=False)
    except Exception:
        return data.hex()


class WdsDecoder:
    def load(self, loader):
        loader.add_option(
            "wds_host", str, "lb-api.wds-stellarium.com", "API host to intercept"
        )
        loader.add_option(
            "wds_out", str, "", "directory to save decoded flows (empty = don't save)"
        )

    def response(self, flow: http.HTTPFlow):
        if (
            flow.response is None
            or ctx.options.wds_host not in flow.request.pretty_host
        ):
            return
        if "/api/" not in flow.request.path:
            return
        path = urlsplit(flow.request.url).path
        record = {
            "path": path,
            "method": flow.request.method,
            "status": flow.response.status_code,
            "request": decode(
                flow.request.raw_content, flow.request.headers.get("Content-Encoding")
            ),
            "response": decode(
                flow.response.raw_content, flow.response.headers.get("Content-Encoding")
            ),
        }
        log.info(json.dumps(record, ensure_ascii=False, indent=2, default=str))
        if ctx.options.wds_out:
            os.makedirs(ctx.options.wds_out, exist_ok=True)
            name = path.strip("/").replace("/", "_") or "root"
            with open(
                os.path.join(ctx.options.wds_out, name + ".json"), "w", encoding="utf-8"
            ) as f:
                json.dump(record, f, ensure_ascii=False, indent=2, default=str)


addons = [WdsDecoder()]
