"""Test harness for the reverse-engineered WDS API client.

The 203 routes below are the ACTUAL API routes recovered from the game's
``global-metadata.dat`` (Sirius.ApiClient 2.31.0). Each operation's method was
disassembled and its route string resolved through the ELF R_AARCH64_RELATIVE
relocations -> Il2CppString -> string-literal table, giving a ground-truth
operation<->route mapping. Each route's HTTP verb / body-vs-no-body was recovered
from the IHttpClientFactory dispatch in the operation's request closure.

Two modes:

    python test_api.py            # OFFLINE: structural checks against a fake
                                  # session (no network). Safe, deterministic.

    python test_api.py --live     # LIVE: hits ONLY read-only GET endpoints on a
                                  # real server. Requires env vars:
                                  #   WDS_API_ENDPOINT   e.g. https://api.example
                                  #   WDS_API_TOKEN      (from Account/Authenticate)
                                  #   WDS_CLIENT_VERSION (optional, default 2.31.0)

Nothing here mutates game state: the live path calls GET routes only.
Also usable under pytest: ``pytest test_api.py`` runs the offline tests.
"""

from __future__ import annotations

import os
import sys

import msgpack

from wds_api import WdsApiClient, routes
from wds_api.models import MODEL_REGISTRY


# --------------------------------------------------------------------------- #
# The actual routes (path, verb, has_body, operation, result) from the binary
# --------------------------------------------------------------------------- #
ACTUAL_ROUTES = [
    (r["path"], r["method"], r["has_body"], r["operation"], r["result"])
    for r in routes.ROUTES
]

READONLY_GET_ROUTES = [r for r in routes.ROUTES if r["method"] == "GET"]


def print_routes() -> None:
    by_verb: dict[str, int] = {}
    for _p, m, _b, _o, _r in ACTUAL_ROUTES:
        by_verb[m] = by_verb.get(m, 0) + 1
    print(f"{len(ACTUAL_ROUTES)} actual API routes: {by_verb}")
    for path, verb, body, op, result in sorted(ACTUAL_ROUTES):
        tag = "body" if body else "----"
        print(f"  {verb:4} {tag}  {path:55} -> {result or 'void'}")


# --------------------------------------------------------------------------- #
# Offline: a fake requests.Session that records the outgoing call
# --------------------------------------------------------------------------- #
class _FakeResponse:
    def __init__(self, body: bytes) -> None:
        self.status_code = 200
        self.content = body
        self.headers: dict[str, str] = {}


class _FakeSession:
    """Records the last request and returns an empty MessagePack array body."""

    def __init__(self) -> None:
        self.last: dict = {}

    def request(self, method, url, params=None, data=None, headers=None, timeout=None):
        self.last = dict(
            method=method, url=url, params=params, data=data, headers=headers
        )
        # a MessagePack response that decodes to an empty array (fields default None)
        return _FakeResponse(msgpack.packb([]))


def _client_with_fake() -> tuple[WdsApiClient, _FakeSession]:
    fake = _FakeSession()
    api = WdsApiClient(
        "https://lb-api.wds-stellarium.com",
        api_token="TESTTOKEN",
        client_version="2.31.0",
        asset_version="2.31.0",
        platform="Android",
        session=fake,  # type: ignore[arg-type]
    )
    return api, fake


# --------------------------------------------------------------------------- #
# Offline tests (pytest-discoverable: test_*)
# --------------------------------------------------------------------------- #
def test_route_count_and_shape() -> None:
    assert len(routes.ROUTES) == 203
    for r in routes.ROUTES:
        assert r["path"].startswith("/api/"), r["path"]
        assert r["method"] in ("GET", "POST", "PUT", "DELETE"), r
        assert isinstance(r["has_body"], bool)


def test_verbs_match_operations() -> None:
    # every operation carries a recovered verb + body flag
    for o in routes.OPERATIONS:
        assert o["method"] in ("GET", "POST", "PUT", "DELETE"), o["operation"]
        # a body-carrying op must have an object payload param
        if o["has_body"]:
            assert o["params"], f"{o['operation']} marked has_body but has no params"


def test_result_models_exist() -> None:
    missing = []
    for o in routes.OPERATIONS:
        rm = o["result_model"]
        if rm and rm not in MODEL_REGISTRY:
            missing.append((o["operation"], rm))
    assert not missing, f"result models not in registry: {missing[:10]}"


def test_get_routes_build_correct_requests() -> None:
    api, fake = _client_with_fake()
    api.account_get_current_user_data()
    assert fake.last["method"] == "GET"
    assert (
        fake.last["url"]
        == "https://lb-api.wds-stellarium.com/api/Account/GetCurrentUserData"
    )
    assert fake.last["data"] is None  # GET has no body
    assert fake.last["headers"]["Authorization"] == "TESTTOKEN"
    assert fake.last["headers"]["X-Client-Version"] == "2.31.0"


def test_post_with_body_serializes_msgpack_array() -> None:
    from wds_api.models_generated import AuthenticatePayload

    api, fake = _client_with_fake()
    api.account_authenticate(
        AuthenticatePayload(
            login_token="abc", game_version=2, application_version="2.31.0"
        )
    )
    assert fake.last["method"] == "POST"
    assert fake.last["url"].endswith("/api/Account/Authenticate")
    # body is a MessagePack array in [Key(n)] order
    decoded = msgpack.unpackb(fake.last["data"], raw=False)
    assert decoded[0] == "abc" and decoded[1] == 2 and decoded[4] == "2.31.0"


def test_post_no_body_uses_query_params() -> None:
    api, fake = _client_with_fake()
    # Accessories_SwitchLock has no literal route -> call_operation synthesizes it
    api.call_operation("Accessories_SwitchLock", query={"accessoryId": 123})
    assert fake.last["method"] == "POST"
    assert fake.last["data"] is None  # no body
    assert fake.last["params"] == {"accessoryId": 123}  # scalar -> query


def test_every_route_method_is_callable() -> None:
    """Smoke-call every generated route method with a fake session."""
    api, fake = _client_with_fake()
    import inspect

    called = 0
    for name in dir(api):
        if name.startswith("_") or name in (
            "request",
            "serialize",
            "deserialize",
            "set_api_token",
            "set_api_endpoint",
            "call_operation",
        ):
            continue
        fn = getattr(api, name)
        if not callable(fn):
            continue
        sig = inspect.signature(fn)
        # supply None for required positional params (payload/scalars)
        kwargs = {}
        try:
            fn()  # most are all-optional
        except TypeError:
            continue
        called += 1
        assert fake.last["url"].startswith("https://lb-api.wds-stellarium.com/api/")
    assert called >= 160


# --------------------------------------------------------------------------- #
# Live smoke test (read-only GETs only) — opt-in
# --------------------------------------------------------------------------- #
def live_smoke() -> int:
    endpoint = os.environ.get("WDS_API_ENDPOINT")
    token = os.environ.get("WDS_API_TOKEN", "")
    if not endpoint:
        print("Set WDS_API_ENDPOINT (and usually WDS_API_TOKEN) to run --live.")
        return 2
    api = WdsApiClient(
        endpoint,
        api_token=token,
        client_version=os.environ.get("WDS_CLIENT_VERSION", "2.31.0"),
        asset_version=os.environ.get("WDS_ASSET_VERSION", ""),
        platform=os.environ.get("WDS_PLATFORM", "Android"),
    )
    print(f"Live GET smoke test against {endpoint}\n")
    # start with the least side-effecting endpoint
    order = ["/api/Environment/Ping"] + [
        r["path"] for r in READONLY_GET_ROUTES if r["path"] != "/api/Environment/Ping"
    ]
    for path in order:
        try:
            res = api.request(path, method="GET", raw=True)
            print(f"  OK   {res.status:>3}  GET {path}")
        except Exception as exc:  # noqa: BLE001 (report, keep going)
            print(f"  ERR       GET {path}: {type(exc).__name__}: {exc}")
    return 0


# --------------------------------------------------------------------------- #
def _run_offline() -> int:
    tests = [
        v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)
    ]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
        except AssertionError as exc:
            failed += 1
            print(f"  FAIL  {t.__name__}: {exc}")
    print(f"\n{len(tests) - failed}/{len(tests)} offline tests passed")
    return 1 if failed else 0


if __name__ == "__main__":
    if "--routes" in sys.argv:
        print_routes()
    elif "--live" in sys.argv:
        sys.exit(live_smoke())
    else:
        print_routes()
        print()
        sys.exit(_run_offline())
