"""Response body decompression, mirroring ``Sirius.Compression``.

The game ships ``BrotliDecompressor`` and ``GZipDecompressor`` (both
``IDecompressor``) selected by a ``DecompressorFactory``. Servers may return
MessagePack bodies compressed with brotli or gzip; the client transparently
decompresses based on the ``Content-Encoding`` response header.
"""

from __future__ import annotations

import gzip
import zlib

try:
    import brotli  # type: ignore

    _HAS_BROTLI = True
except ImportError:  # pragma: no cover
    brotli = None  # type: ignore
    _HAS_BROTLI = False


def decompress(body: bytes, content_encoding: str | None) -> bytes:
    """Decompress ``body`` according to ``content_encoding`` (case-insensitive).

    Unknown/empty encodings are returned unchanged (the transport already
    lets the HTTP layer handle standard transfer decoding).
    """
    enc = (content_encoding or "").strip().lower()
    if enc in ("", "identity"):
        return body
    if enc == "br":
        if not _HAS_BROTLI:
            raise RuntimeError(
                "brotli-encoded response but the 'brotli' package is not installed"
            )
        return brotli.decompress(body)
    if enc == "gzip":
        return gzip.decompress(body)
    if enc == "deflate":
        return zlib.decompress(body)
    return body
