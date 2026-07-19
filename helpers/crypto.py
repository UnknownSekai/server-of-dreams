"""Encryption for WDS downloadable assets (notation charts, music configs).

Files under ``/Notations/{music}/{difficulty}.enc`` and ``.../music_config.enc`` are
AES-256-CBC with the IV prepended as the first 16 bytes. Both decrypt to CSV, but the
keys and post-processing differ (both keys are baked into libil2cpp):

    notation:     brotli.decompress(decrypt_aes(content, NOTATION_KEY))  -> note chart
    music_config: decrypt_aes(content, MUSIC_CONFIG_KEY)                 -> cue-sheet CSV
"""

import os
from typing import Optional

import brotli
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# keys baked into the client (libil2cpp) for downloadable assets
NOTATION_KEY = b"k8teTB%QH.v-hY+e)7wees8bxYSLQdAg"
MUSIC_CONFIG_KEY = b"X)|9Vs+&AB5qKBrzqWq)quqEjFug8LaK"

_BLOCK = 16


def _pkcs7_pad(data: bytes) -> bytes:
    pad = _BLOCK - (len(data) % _BLOCK)
    return data + bytes([pad]) * pad


def _pkcs7_unpad(data: bytes) -> bytes:
    pad = data[-1]
    if not 1 <= pad <= _BLOCK or data[-pad:] != bytes([pad]) * pad:
        raise ValueError("invalid PKCS7 padding")
    return data[:-pad]


def decrypt_aes(content: bytes, key: bytes) -> bytes:
    """AES-CBC decrypt; the first 16 bytes of ``content`` are the IV."""
    iv, ciphertext = content[:_BLOCK], content[_BLOCK:]
    dec = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
    return _pkcs7_unpad(dec.update(ciphertext) + dec.finalize())


def encrypt_aes(plaintext: bytes, key: bytes, iv: Optional[bytes] = None) -> bytes:
    """AES-CBC encrypt, prepending the IV (random if not given) to the ciphertext."""
    if iv is None:
        iv = os.urandom(_BLOCK)
    enc = Cipher(algorithms.AES(key), modes.CBC(iv)).encryptor()
    return iv + enc.update(_pkcs7_pad(plaintext)) + enc.finalize()


def decrypt_notation(content: bytes, key: bytes = NOTATION_KEY) -> bytes:
    """Decrypt + brotli-decompress a notation/config asset to its raw bytes."""
    return brotli.decompress(decrypt_aes(content, key))


def encrypt_notation(
    data: bytes, key: bytes = NOTATION_KEY, iv: Optional[bytes] = None
) -> bytes:
    """brotli-compress + AES-encrypt raw bytes back into a notation asset."""
    return encrypt_aes(brotli.compress(data), key, iv)


def decrypt_music_config(content: bytes, key: bytes = MUSIC_CONFIG_KEY) -> bytes:
    """Decrypt a music_config asset to its raw cue-sheet CSV bytes (no compression)."""
    return decrypt_aes(content, key)


def encrypt_music_config(
    data: bytes, key: bytes = MUSIC_CONFIG_KEY, iv: Optional[bytes] = None
) -> bytes:
    """AES-encrypt raw cue-sheet CSV bytes back into a music_config asset."""
    return encrypt_aes(data, key, iv)
