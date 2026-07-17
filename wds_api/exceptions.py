"""Exceptions mirroring ``Sirius.Api.ApiActionException`` and HTTP failures."""

from __future__ import annotations

from typing import Optional


class ApiActionException(Exception):
    """Mirror of ``Sirius.Api.ApiActionException`` (fields as reversed).

    Status/flag semantics come from ``ApiClient``:
      * 401  -> illegal login          (is_http_error)
      * 403  -> maintenance            (is_http_error)
      * 440  -> login timed out        (is_http_error)
      * network layer failure          -> is_network_error
      * request cancelled              -> is_cancel
      * request timed out              -> is_timeout
    """

    def __init__(
        self,
        status: int,
        error_message: str = "",
        *,
        is_http_error: bool = False,
        is_network_error: bool = False,
        is_cancel: bool = False,
        is_critical: bool = False,
        is_timeout: bool = False,
    ) -> None:
        super().__init__(f"[{status}] {error_message}")
        self.status = status
        self.error_message = error_message
        self.is_http_error = is_http_error
        self.is_network_error = is_network_error
        self.is_cancel = is_cancel
        self.is_critical = is_critical
        self.is_timeout = is_timeout

    # ApiClient treats these HTTP codes specially.
    HTTP_ILLEGAL_LOGIN = 401
    HTTP_MAINTENANCE = 403
    HTTP_LOGIN_TIMEOUT = 440

    @property
    def is_illegal_login(self) -> bool:
        return self.status == self.HTTP_ILLEGAL_LOGIN

    @property
    def is_maintenance(self) -> bool:
        return self.status == self.HTTP_MAINTENANCE

    @property
    def is_login_timeout(self) -> bool:
        return self.status == self.HTTP_LOGIN_TIMEOUT


class NotAllowedVersionException(ApiActionException):
    """Raised when the client/asset version is rejected by the version checker.

    Mirrors ``ApiActionException.NotAllowedVersion()``.
    """

    def __init__(self, message: str = "client version not allowed") -> None:
        super().__init__(-1, message, is_critical=True)
