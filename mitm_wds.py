import gzip
import io
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
try:
    import lz4.block
except ImportError:
    lz4 = None

log = logging.getLogger("wds")


def _lz4_decompress(code, data):
    if code == 99:  # Lz4Block: msgpack int (uncompressed length) + LZ4 block
        up = msgpack.Unpacker(raw=False)
        up.feed(data)
        length = up.unpack()
        return lz4.block.decompress(data[up.tell() :], uncompressed_size=length)
    # code == 98 Lz4BlockArray: array [lengths_or_totallength, block, block, ...]
    arr = msgpack.unpackb(data, raw=False)
    lengths, blocks = arr[0], arr[1:]
    if not isinstance(lengths, (list, tuple)):
        lengths = [lengths] * len(blocks)
    return b"".join(
        lz4.block.decompress(b, uncompressed_size=n) for n, b in zip(lengths, blocks)
    )


def _unwrap_lz4(obj):
    if isinstance(obj, msgpack.ExtType) and obj.code in (98, 99) and lz4:
        return _unwrap_lz4(
            msgpack.unpackb(
                _lz4_decompress(obj.code, obj.data), raw=False, strict_map_key=False
            )
        )
    return obj


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
        objs = [
            _unwrap_lz4(o)
            for o in msgpack.Unpacker(io.BytesIO(data), raw=False, strict_map_key=False)
        ]
    except Exception:
        return data.hex()
    return objs[0] if len(objs) == 1 else objs


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
