"""AES payload crypto — a faithful re-implementation of
``Plugins.Sirius.Security.Cryptography.CustomAesEncoder`` from the game binary.

Reversed from ``libil2cpp.so`` (app 2.31.0). The original C# methods are
compiled to native code; the algorithm below is reconstructed from the ARM64
disassembly of ``CustomAesEncoder.CreateWithInitialize / Encrypt / Decrypt``.

Reconstructed algorithm
-----------------------
``CreateWithInitialize(iv, password)`` builds an AES instance with::

    Aes.Create()
    aes.BlockSize = 128
    aes.KeySize   = 256                 # AES-256
    aes.Mode      = CipherMode.CBC      # (enum value 1)
    aes.Padding   = PaddingMode.PKCS7   # (enum value 2)
    aes.IV        = iv                  # 16 bytes
    aes.Key       = Encoding.UTF8.GetBytes(password)   # password must be 32 chars

``Encrypt(password, data)``::

    salt = new byte[8]                  # eight 0x00 bytes, never filled
    iv   = new Rfc2898DeriveBytes(data, salt, 1000, HashAlgorithmName.SHA256)
               .GetBytes(16)            # PBKDF2-HMAC-SHA256, KDF input == plaintext
    ct   = aes(iv, password).CreateEncryptor().TransformFinalBlock(data)
    return iv.Concat(ct).ToArray()      # 16-byte IV prepended to ciphertext

``Decrypt(password, data)``::

    iv   = data[:16]
    ct   = data[16:]
    return aes(iv, password).CreateDecryptor().TransformFinalBlock(ct)  # PKCS7-unpadded

IMPORTANT — where this is actually used
---------------------------------------
An xref scan of the binary shows ``Encrypt`` has **zero** call sites and
``Decrypt`` is called from exactly two:

    Sirius.DebugMusicConfigFactory.<LoadWebAsync>
    Sirius.DebugNotationFactory.<LoadWebAsync>

i.e. this cipher only guards a couple of *debug* web-loaded resources (music
config / chart notation). The main game API (``Sirius.ApiClient``) does **not**
apply this cipher to request/response bodies — those go over HTTPS as plain
MessagePack (optionally Brotli/GZip compressed). See ``transport.py``.

The debug password (a 32-char string) is loaded from a static field the dump
tables don't catalogue, so it is left as a required argument rather than
guessed.
"""

from __future__ import annotations

import hashlib

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives.padding import PKCS7
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "wds_api.crypto requires the 'cryptography' package (pip install cryptography)"
    ) from exc

BLOCK_BITS = 128
KEY_BITS = 256
IV_BYTES = 16
PBKDF2_SALT = b"\x00" * 8  # CustomAesEncoder uses an all-zero 8-byte salt
PBKDF2_ITERATIONS = 1000  # 0x3E8


def _key_from_password(password: str) -> bytes:
    key = password.encode("utf-8")
    if len(key) != KEY_BITS // 8:
        raise ValueError(
            f"password must encode to exactly {KEY_BITS // 8} UTF-8 bytes for AES-256, "
            f"got {len(key)}"
        )
    return key


def _derive_iv(data: bytes) -> bytes:
    """IV = PBKDF2-HMAC-SHA256(plaintext, salt=0x00*8, iters=1000)[:16].

    Faithful to the binary: the KDF input is the *plaintext* ``data`` (the
    ``byte[]`` Rfc2898DeriveBytes overload). Because the IV is prepended to the
    output, decryption never needs to recompute it.
    """
    return hashlib.pbkdf2_hmac(
        "sha256", data, PBKDF2_SALT, PBKDF2_ITERATIONS, dklen=IV_BYTES
    )


def encrypt(password: str, data: bytes) -> bytes:
    """AES-256-CBC/PKCS7 encrypt; returns ``iv(16) || ciphertext``."""
    key = _key_from_password(password)
    iv = _derive_iv(data)
    padder = PKCS7(BLOCK_BITS).padder()
    padded = padder.update(data) + padder.finalize()
    enc = Cipher(algorithms.AES(key), modes.CBC(iv)).encryptor()
    ct = enc.update(padded) + enc.finalize()
    return iv + ct


def decrypt(password: str, data: bytes) -> bytes:
    """Inverse of :func:`encrypt`. Reads the 16-byte IV from the prefix."""
    if len(data) < IV_BYTES:
        raise ValueError("ciphertext too short to contain a 16-byte IV prefix")
    key = _key_from_password(password)
    iv, ct = data[:IV_BYTES], data[IV_BYTES:]
    dec = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
    padded = dec.update(ct) + dec.finalize()
    unpadder = PKCS7(BLOCK_BITS).unpadder()
    return unpadder.update(padded) + unpadder.finalize()


class CustomAesEncoder:
    """Object-style mirror of the C# ``CustomAesEncoder`` class."""

    IvBytes = IV_BYTES

    def Encrypt(self, password: str, data: bytes) -> bytes:  # noqa: N802 (mirror C#)
        return encrypt(password, data)

    def Decrypt(self, password: str, data: bytes) -> bytes:  # noqa: N802 (mirror C#)
        return decrypt(password, data)
