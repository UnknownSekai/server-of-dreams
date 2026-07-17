"""Core HTTP transport — a faithful port of ``Sirius.Api.ApiClient``'s pipeline.

Confirmed from the IL2CPP dump + ARM64 disassembly (app 2.31.0):

* **Base URL**  every request URL is ``api_endpoint + "/api/<Controller>/<Action>"``.
  ``api_endpoint`` is bootstrapped, then replaced by
  ``EnvironmentResult.ApiEndpoint`` returned by ``Environment/GetEnvironment``.
* **Verb**  chosen per operation via ``IHttpClientFactory`` (Get/Post/Put/Delete).
* **Body**  ``MessagePackSerializer.Serialize(payload)`` — standard MessagePack,
  DTOs are integer-``[Key]`` arrays (see ``models.py``). No app-layer encryption
  on API bodies (only TLS); the AES in ``crypto.py`` guards debug resources only.
* **Request headers**  ``X-Client-Version``, ``X-Assets-Version``, ``X-Platform``,
  ``Authorization`` (the API token).
* **Response headers**  the client reads ``X-Server-Version``, ``X-Maintenance``,
  ``X-Maintenance-Message``, ``X-Token-Expired``, ``X-MasterData-*``, ``X-FM``,
  ``date`` and ``x-timewarp-date`` to drive app state.
* **Errors**  HTTP 401 = illegal login, 403 = maintenance, 440 = login timeout;
  plus network / timeout / cancel classification.
* **Retry**  up to 3 attempts, 1000 ms interval, 5000 ms max due (constants from
  the binary).
"""

from __future__ import annotations

import time
from typing import Any, Callable, Optional

import msgpack
import requests

from .compression import decompress
from .exceptions import ApiActionException
from .models import ApiActionResult, Headers

# ApiClient constants (from the binary)
RETRY_COUNT = 3
RETRY_INTERVAL_MS = 1000
RETRY_MAX_DUE_MS = 5000
HTTP_ILLEGAL_LOGIN = 401
HTTP_MAINTENANCE = 403
HTTP_LOGIN_TIMEOUT = 440


class SiriusApiClient:
    """Low-level client: builds/sends requests, decodes MessagePack, tracks state.

    Parameters
    ----------
    api_endpoint:
        Base URL, e.g. the value returned in ``EnvironmentResult.ApiEndpoint``.
        Routes from ``routes.py`` are appended to it.
    api_token:
        Value sent in the ``Authorization`` header. Obtained from
        ``Account/Authenticate`` (``AuthenticateResult.Token``).
    client_version / asset_version:
        Sent as ``X-Client-Version`` / ``X-Assets-Version`` (e.g. ``"2.31.0"``).
    platform:
        ``X-Platform`` value — ``"Android"`` or ``"iPhone"`` in the binary.
    auth_scheme:
        Prefix for the Authorization header. Default ``""`` sends the raw token;
        set to ``"Bearer "`` if the server expects a scheme.
    """

    #: Production API host, recovered from the Unity config asset ``sharedassets0.assets``
    #: (``lb-api`` = load-balanced API). Requests go to ``{DEFAULT_API_ENDPOINT}/api/<...>``.
    #: It is NOT in the IL2CPP metadata — the client loads it from a config asset at runtime,
    #: then may replace it with ``EnvironmentResult.ApiEndpoint`` from ``Environment/GetEnvironment``.
    DEFAULT_API_ENDPOINT = "https://lb-api.wds-stellarium.com"

    def __init__(
        self,
        api_endpoint: str = DEFAULT_API_ENDPOINT,
        *,
        api_token: str = "",
        client_version: str = "2.31.0",
        asset_version: str = "",
        platform: str = "Android",
        auth_scheme: str = "",
        session: Optional[requests.Session] = None,
        timeout: float = 30.0,
        retry_count: int = RETRY_COUNT,
        retry_interval_ms: int = RETRY_INTERVAL_MS,
    ) -> None:
        self.api_endpoint = api_endpoint.rstrip("/")
        self.api_token = api_token
        self.client_version = client_version
        self.asset_version = asset_version
        self.platform = platform
        self.auth_scheme = auth_scheme
        self.timeout = timeout
        self.retry_count = retry_count
        self.retry_interval_ms = retry_interval_ms
        self._session = session or requests.Session()

        # state populated from response headers (mirrors ApiClient properties)
        self.last_server_version: str = ""
        self.maintenance: bool = False
        self.maintenance_message: str = ""
        self.maintenance_endpoint: str = ""
        self.token_expired: bool = False
        self.feature_maintenance_flags: str = ""
        self.master_data_version: str = ""
        self.master_data_uri: str = ""
        self.master_data_sas_token: str = ""
        self.master_data_publish_timestamp: str = ""
        self.response_date: str = ""
        self.timewarp_date: str = ""

    # -- token -----------------------------------------------------------------
    def set_api_token(self, token: str) -> None:
        self.api_token = token

    def set_api_endpoint(
        self, api_endpoint: str, maintenance_endpoint: str = ""
    ) -> None:
        self.api_endpoint = api_endpoint.rstrip("/")
        self.maintenance_endpoint = maintenance_endpoint

    # -- serialization ---------------------------------------------------------
    @staticmethod
    def serialize(payload: Any) -> bytes:
        """MessagePack-encode a payload (``MsgpackModel`` -> array, else as-is)."""
        if payload is None:
            return b""
        if hasattr(payload, "to_array"):
            payload = payload.to_array()
        return msgpack.packb(payload, use_bin_type=True) or b""

    @staticmethod
    def deserialize(data: bytes) -> Any:
        if not data:
            return None
        return msgpack.unpackb(data, raw=False, strict_map_key=False)

    # -- headers ---------------------------------------------------------------
    def _build_headers(self, has_body: bool) -> dict[str, str]:
        h: dict[str, str] = {
            Headers.CLIENT_VERSION: self.client_version,
            Headers.ASSET_VERSION: self.asset_version,
            "X-Platform": self.platform,
        }
        if self.api_token:
            h["Authorization"] = f"{self.auth_scheme}{self.api_token}"
        if has_body:
            h["Content-Type"] = "application/x-msgpack"
        h["Accept"] = "application/x-msgpack"
        return h

    def _read_response_headers(self, resp: requests.Response) -> None:
        g = resp.headers.get
        self.last_server_version = g(Headers.SERVER_VERSION, self.last_server_version)
        if g(Headers.MAINTENANCE) is not None:
            self.maintenance = g(Headers.MAINTENANCE) not in ("", "0", "false", "False")
        self.maintenance_message = g(
            Headers.MAINTENANCE_MESSAGE, self.maintenance_message
        )
        if g(Headers.TOKEN_EXPIRED) is not None:
            self.token_expired = g(Headers.TOKEN_EXPIRED) not in (
                "",
                "0",
                "false",
                "False",
            )
        self.feature_maintenance_flags = g(
            Headers.FEATURE_MAINTENANCE, self.feature_maintenance_flags
        )
        self.master_data_version = g(
            Headers.MASTERDATA_VERSION, self.master_data_version
        )
        self.master_data_uri = g(Headers.MASTERDATA_URI, self.master_data_uri)
        self.master_data_sas_token = g(
            Headers.MASTERDATA_SAS_TOKEN, self.master_data_sas_token
        )
        self.master_data_publish_timestamp = g(
            Headers.MASTERDATA_PUBLISH_TIMESTAMP, self.master_data_publish_timestamp
        )
        self.response_date = g(Headers.DATE, self.response_date)
        self.timewarp_date = g(Headers.TIMEWARP_DATE, self.timewarp_date)

    # -- core request ----------------------------------------------------------
    def _resolve_result(
        self, decoded: Any, result_model: Optional[str], result_is_array: bool
    ) -> Any:
        if result_model is None or decoded is None:
            return decoded
        from .models import MODEL_REGISTRY

        cls = MODEL_REGISTRY.get(result_model)
        if cls is None:
            return decoded
        if result_is_array and isinstance(decoded, (list, tuple)):
            return [cls.from_array(x) for x in decoded]
        return cls.from_array(decoded)

    def request(
        self,
        path: str,
        *,
        method: str = "POST",
        payload: Any = None,
        query: Optional[dict] = None,
        result_model: Optional[str] = None,
        result_is_array: bool = False,
        result_factory: Optional[Callable[[Any], Any]] = None,
        raw: bool = False,
    ) -> ApiActionResult:
        """Send one request (with retry) and return an :class:`ApiActionResult`.

        ``payload`` is MessagePack-encoded into the body (POST-with-body ops).
        ``query`` holds scalar args for no-body POST/GET ops (sent as query string).
        ``result_model`` names a class in ``models_generated`` used to decode the
        response array; ``result_factory`` is an explicit override. ``raw`` returns
        the undecoded MessagePack object.
        """
        url = (
            self.api_endpoint + path
            if path.startswith("/")
            else f"{self.api_endpoint}/{path}"
        )
        body = self.serialize(payload) if payload is not None else None
        headers = self._build_headers(has_body=body is not None)
        params = {k: v for k, v in (query or {}).items() if v is not None} or None

        attempt = 0
        while True:
            attempt += 1
            try:
                resp = self._session.request(
                    method.upper(),
                    url,
                    params=params,
                    data=body,
                    headers=headers,
                    timeout=self.timeout,
                )
            except requests.Timeout as exc:
                if attempt <= self.retry_count:
                    time.sleep(self.retry_interval_ms / 1000)
                    continue
                raise ApiActionException(
                    -1, str(exc), is_timeout=True, is_network_error=True
                ) from exc
            except requests.RequestException as exc:
                if attempt <= self.retry_count:
                    time.sleep(self.retry_interval_ms / 1000)
                    continue
                raise ApiActionException(-1, str(exc), is_network_error=True) from exc

            self._read_response_headers(resp)
            content = decompress(resp.content, resp.headers.get("Content-Encoding"))

            if resp.status_code >= 400:
                # retry 5xx only; 4xx are terminal app errors
                if resp.status_code >= 500 and attempt <= self.retry_count:
                    time.sleep(self.retry_interval_ms / 1000)
                    continue
                msg = self._error_message(content)
                raise ApiActionException(
                    resp.status_code,
                    msg,
                    is_http_error=True,
                    is_critical=resp.status_code
                    in (HTTP_ILLEGAL_LOGIN, HTTP_MAINTENANCE, HTTP_LOGIN_TIMEOUT),
                )

            decoded = self.deserialize(content)
            if raw:
                response_obj = decoded
            elif result_factory is not None and decoded is not None:
                response_obj = result_factory(decoded)
            else:
                response_obj = self._resolve_result(
                    decoded, result_model, result_is_array
                )
            return ApiActionResult(status=resp.status_code, response=response_obj)

    def _error_message(self, content: bytes) -> str:
        try:
            decoded = self.deserialize(content)
            if isinstance(decoded, (list, tuple)) and decoded:
                return str(decoded[0])
            return str(decoded)
        except Exception:
            return content[:200].decode("utf-8", "replace")
