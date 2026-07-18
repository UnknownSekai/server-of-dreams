# wds_api — reverse-engineered World Dai Star API client (thanks claude)

Python port of the game's `Sirius.ApiClient` (app **2.31.0**), reconstructed from
the IL2CPP dump (`dump.cs`, `script.json`, `stringliteral.json`) and ARM64
disassembly of `libil2cpp.so`.

## Install

```bash
pip install -r wds_api/requirements.txt   # requests, msgpack, cryptography, brotli
```

## Layout

| module                | contents |
|-----------------------|----------|
| `transport.py`        | `SiriusApiClient` — request pipeline: base URL, headers, MessagePack, auth token, retry, response-header state, error mapping, result decoding. |
| `client.py`           | `WdsApiClient` — one method per discovered route + `call_operation()` for all 468 ops. |
| `routes.py`           | `ROUTES` (203, ground-truth) + `OPERATIONS` (468) catalog, each with **recovered** verb/body/result. |
| `models_generated.py` | **263 request/response DTOs + 69 enums** with `[Key(n)]` layouts (`from_array`/`to_array`). |
| `models.py`           | `ApiActionResult`, header constants, `MsgpackModel` base (recursive decode). |
| `crypto.py`           | `CustomAesEncoder` — AES-256-CBC/PKCS7 (debug resources only, see below). |
| `compression.py`      | Brotli/GZip response decompression. |
| `exceptions.py`       | `ApiActionException`. |

## Usage

```python
from wds_api import WdsApiClient
from wds_api.models_generated import AuthenticatePayload, AuthenticateResult, UserResult

api = WdsApiClient(client_version="2.31.0", platform="Android")

res = api.account_authenticate(AuthenticatePayload(login_token="...", application_version="2.31.0"))
api.set_api_token(res.response.token)          # response is a decoded AuthenticateResult

user = api.account_get_current_user_data()     # GET; response decoded to UserResult
sw   = api.call_operation("Accessories_SwitchLock", query={"accessoryId": 123})  # any of 468 ops
```

## What was recovered from the binary

* **HTTP verb + body/no-body** — *recovered, not guessed.* Every operation's
  request-building closure was disassembled and classified by which
  `IHttpClientFactory` method it dispatches:
  * `Get(uri, serializer)` → **GET** (28 routes / 47 ops)
  * `Post(uri, serializer)` → **POST, no body**, scalar args in the URL (75 / 304)
  * `Post<T>(uri, value, serializer)` → **POST with a MessagePack body** (100 / 117)
  (`Put`/`Delete` exist in the factory but are unused.)
* **Routes** — 203, mapped to operations by *ground truth*: each method's route
  string was resolved through the ELF `R_AARCH64_RELATIVE` relocations →
  `Il2CppString` → string-literal table (no name-guessing). 34 are query-template
  routes (`?circleId=`, `?targetUserId=`, …).
* **Request/response models** — 263 DTOs + 69 enums extracted with their integer
  `[Key(n)]` order, so bodies serialize and responses decode as MessagePack
  **arrays in key order** (nested models and enums decode recursively).
* **Base URL** — `https://lb-api.wds-stellarium.com` (default), giving
  `https://lb-api.wds-stellarium.com/api/<Controller>/<Action>`. This host is **not**
  in the code metadata; it lives in the Unity config asset `sharedassets0.assets`
  and is loaded at runtime, then may be replaced by `EnvironmentResult.ApiEndpoint`
  from `Environment/GetEnvironment`.
* **Headers** — request: `X-Client-Version`, `X-Assets-Version`, `X-Platform`,
  `Authorization`. Response state consumed: `X-Server-Version`, `X-Maintenance*`,
  `X-Token-Expired`, `X-MasterData-*`, `X-FM`, `date`, `x-timewarp-date`.
* **Errors / retry** — 401 illegal login, 403 maintenance, 440 login timeout;
  3 retries / 1000 ms / 5000 ms.

## Encryption / decryption

`crypto.py` faithfully reproduces `CustomAesEncoder`:

```
key = UTF8(password)                              # 32 bytes -> AES-256
iv  = PBKDF2-HMAC-SHA256(plaintext, salt=0x00*8, iters=1000)[:16]
out = iv(16) || AES-CBC/PKCS7(key, iv, plaintext) # IV prepended
```

An xref scan proves this cipher is used **only** by `DebugMusicConfigFactory` /
`DebugNotationFactory` for debug web-loaded music/chart data (`Encrypt` has zero
call sites). **The main API does not encrypt bodies** — confidentiality is TLS,
bodies are plain (optionally Brotli/GZip) MessagePack.

## Remaining caveats

* **URL placement of scalar args** (no-body POST / GET) is *not* encoded in the
  dump, so those are sent as **query parameters**; some endpoints may expect path
  segments. Pass `path=`/`query=` to `call_operation`, or `method=` to any method.
* **~265 operations have no string-literal route** in the binary (dynamic paths);
  `call_operation` synthesizes `/api/<Feature>/<Action>` for them (marked
  unverified) — override `path=` if needed. The 203 ground-truth routes are exact.
* Not tested against live servers — this is a research/interop reconstruction.
