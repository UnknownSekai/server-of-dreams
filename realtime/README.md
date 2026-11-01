# Realtime channel (StreamingHub)

Server of Dreams speaks two protocols. The REST API in `routes/` is the one the client
uses for everything outside a live: login, characters, shops, gacha. This package is the
**other** one — the realtime channel the game opens when it enters a multi-live, a circle
chat, or collects friend invitations.

They are genuinely different: different port, different protocol, different auth path.
The API is HTTP/1.1 JSON-ish MessagePack over FastAPI; this is **HTTP/2 + gRPC carrying
MagicOnion StreamingHub frames** on a long-lived bidirectional stream.

## Why it is not an ASGI route

A StreamingHub call is one stream that lives for the whole session:

* the response headers must be sent **before** any request body, because the client sends
  `end_stream=false` with an empty body and then waits;
* a request body may never arrive at all — `Connect` is a stream, not a request/response
  pair;
* messages flow both ways for as long as the stream lives.

Uvicorn buffers the request body, which reproduces exactly the hang that made this channel
impossible to proxy through mitmproxy. So the transport is written directly on `h2`
(`transport.py`), and it works.

## Layout

| Module | Responsibility |
| --- | --- |
| `framing.py` | gRPC frames; MagicOnion message shapes; LZ4 compression both ways |
| `methods.py` | FNV1A32 method ids, per hub |
| `dtos.py` | wire DTOs in MessagePack-CSharp array form |
| `state.py` | connections, **seats**, rooms, broadcast fan-out |
| `hub.py` | the handlers — the actual game logic |
| `transport.py` | HTTP/2 + TLS server on `h2` |
| `dispatcher.py` | binds a frame to a handler, authenticates, owns the service |

## Running it

```bash
.venv/bin/python realtime_main.py          # standalone, the usual way
```

Or in the same process as the API, by setting `realtime.auto_start: true` in `config.yml`.
Both are supported; standalone is easier to test and restart.

`config.yml`:

```yaml
realtime:
  host: 0.0.0.0
  port: 8443
  certfile: cert.pem
  keyfile:  key.pem
  auto_start: false
```

TLS needs **both** files; with neither the channel serves cleartext, which is only useful
for a local test.

### Generating SSL/TLS Certificates

The realtime StreamingHub runs over HTTP/2 with ALPN (`h2`). For local development, testing, or self-hosted environments you need a self-signed certificate and private key.

The simplest way needs **no `openssl` binary** — it uses the OpenSSL bundled inside the `cryptography` wheel:

```bash
python -m scripts.generate_realtime_cert
```

It reads the realtime hostname from `multi_real_time_server_url` in `config.yml`, writes
`certs/realtime-cert.pem` and `certs/realtime-key.pem` (rsa:4096, sha256, self-signed, 365
days) with `subjectAltName=DNS:<host>,DNS:localhost,IP:127.0.0.1`, and verifies the pair
loads for TLS `h2`. Override with `--host`, `--cert`, `--key`, `--days`, or `--force`.

The cert can cover more than one name. The client accepts it for any host in its SAN, so add
every hostname/IP it might connect to — a future online host, a LAN address — and each is
auto-detected as DNS or IP:

```bash
python -m scripts.generate_realtime_cert --host lb-realtime.wds-stellarium.com --host rt.example.com --host 192.168.1.50
```

The first `--host` becomes the CN; `localhost` + `127.0.0.1` are always added. To make extra
names permanent (applied on every regenerate), list them under `realtime.cert_hosts` in
`config.yml`:

```yaml
realtime:
  cert_hosts: ["rt.example.com", "192.168.1.50"]
```

Or, if you already have OpenSSL installed:

```bash
openssl req -x509 -newkey rsa:4096 -nodes -sha256 \
  -keyout key.pem -out cert.pem -days 365 \
  -subj "/CN=your-realtime-domain.com" \
  -addext "subjectAltName=DNS:your-realtime-domain.com,DNS:localhost,IP:127.0.0.1"
```

> **Note:**
> - Adjust the `CN` (Common Name) and `subjectAltName` (SAN) to match the hostname or IP configured in your `config.yml` (`multi_real_time_server_url`).
> - If deploying behind a reverse proxy (e.g. Caddy, Nginx, Cloudflare) that terminates TLS and proxies HTTP/2 to the realtime server, configure TLS upstream accordingly or serve cleartext HTTP/2 locally.

Point the client at this listener through `multi_real_time_server_url` in `/api/Environment`
(`multi_real_time_server_url` in `config.yml`).

## The protocol, as observed

Everything here is reconstructed from a **captured live session**, so shapes are
evidence-backed rather than inferred. The facts that cost the most to establish:

**Method ids are a hash, not a position.** `id = FNV1A32(methodName)` reinterpreted as a
signed int32. The name hashed is the bare declaration — no interface prefix, the `Async`
suffix kept. Verified against every id that appeared in the capture. A method id does
**not** identify a hub on its own: `JoinAsync` and `OnJoin` hash the same in two different
interfaces, so an id must always be paired with the hub it arrived on.

**Framing.** `flag(1) + length(4, big-endian) + payload`, where the payload is a MessagePack
array. `[MessageId, MethodId, args]` is a request from the client and a response from the
server — the same shape, disambiguated by direction. `[MethodId, args]` is a broadcast
(receiver callback) with **no message id**, which is exactly what makes it distinguishable.
`[-1, 0, nil]` (`0x93 0xff 0x00 0x0c`) is a marker the server sends first: the client
ignores it, a proxy needs it to flush instead of buffering.

**Every request gets a response**, including void methods, which answer `nil`. Missing that
leaves the client's `UniTask` pending forever.

**The client requires at least one frame after the headers.** `ConnectAsync` throws
"failed to negotiate with the server" if `MoveNext` completes without data, so the marker
frame is load-bearing, not cosmetic.

**Compression is on the argument, not the frame.** A large argument list arrives as
`[ExtType(98), block]` *in place of* the arguments, and a large reply as `[ExtType(99)]`.
Decoding order matters: decompress **before** flattening ext types, or the payload becomes
unrecognisable.

**Seats and disconnections.** While a game is actively in progress (`room.game_started`),
a temporary disconnect keeps the seat (`unbind`), snapshotting state so a quick mid-game
reconnect can recover and submit results. Outside an active live (in the lobby, result screen,
or when moving to another hall via `_detach`), leaving removes the member from `room.members`
(`remove_member`) and broadcasts `OnLeaveAnyOne`, freeing the seat so other players see the
empty slot immediately and preventing multi-room ghost profiles. Only `IMultiLiveHub` owns
seats — a circle or common-hub connection for the same account must not take one over.

**Hall type and size.** `13` = Gingaza (public), `21` = team challenge, `11`/`12`/`14`/`15`
are the other halls. Four members maximum. A public join replies with a **nil** hall id
(public rooms are addressed server-side); a private one returns its id.

## DTO layouts

MessagePack-CSharp writes `[MessagePackObject]` types as **arrays indexed by `[Key(n)]`**,
not maps. Field order is load-bearing: one field wrong shifts every following value and the
client misreads silently. Lengths, each confirmed against the capture:

* `MultiLiveCharacter` — **11**
* `MultiLiveUser` — **14**
* `CircleChat` — **11**
* `CircleActivityLog` — **8**
* `MultiLiveInvitation` — **13**
* `MultiLiveCreatePrivateHallResult` — 5, `MultiLiveJoinResult` — 6,
  `MultiLiveFetchUsersResult` — 3

## Tests

```bash
.venv/bin/python -m realtime.test_realtime   # End-to-end checks over a real HTTP/2 connection
```

`test_realtime` drives a whole two-player session end to end: create a private hall, a
guest joins by key code, ready/decide, music and difficulty, game start, in-game sync, exit,
final results, continue play, leave, invitations, seat ownership across reconnects.

## What is verified, and what is not

Verified against the live listener with real tokens and real game clients (patched Android APK):

* TLS + ALPN `h2` negotiate; a token minted by `make_session_jwt` is accepted and maps to
  the right user id; a forged token is refused;
* create hall → guest joins by key code → host receives `OnJoin` → `FetchUsersAsync` returns
  both members → ready/decide (or auto-advance on all ready / full room) → `OnReadyGroup` and `OnGoGame`
  out to everyone;
* synchronized music lottery (`OnLotMusic`), synchronized difficulty selection (`OnGoGame`),
  `ReadyGameAsync` sync → `OnPlayGame` countdown and live gameplay;
* in-game note status sync (`SyncInGameStatusAsync`), live finish (`ExitGameAsync`), final results
  broadcast (`OnExitAllGames` with MVP IDs and synchronized 60-second result timer);
* continue play (`ContinuePlayAsync`) keeps the hall while correctly leaving other members in
  confirming state until they also continue or leave.

## What is not verified:

* chat history and the circle activity log are **in memory only** and start empty; the
  capture's non-empty pages are real server data we do not reproduce;
* `GetActivityLogsAsync` returns empty because nothing records activity yet;
* friend invitations are keyed by user id parsed from the client's friend-id strings; the
  real server's friend graph is not modelled, so an invitation only reaches a friend whose
  id happens to be a known account;
* player rank, trophies and icon frames in an invitation are placeholders (`0`), because the
  account data that would fill them is not read yet.
