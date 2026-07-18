"""wds_api — reverse-engineered Python client for the World Dai Star:
Yume no Stellarium game API (app 2.31.0, ``Sirius.ApiClient``).

Quick start
-----------
    from wds_api import WdsApiClient
    from wds_api.models_generated import AuthenticatePayload, AuthenticateResult

    api = WdsApiClient(
        api_endpoint="https://lb-api.wds-stellarium.com",  # default; from config asset
        client_version="2.31.0",
        platform="Android",
    )
    res = api.account_authenticate(
        AuthenticatePayload(login_token="...", game_version=0, application_version="2.31.0"),
        raw=False,
    )
    token = AuthenticateResult.from_array(res.response).token
    api.set_api_token(token)

    user = api.account_get_current_user_data(raw=True)   # decoded MessagePack array

See ``README.md`` for the transport/crypto details and caveats.
"""

from __future__ import annotations

from . import crypto, decode, models_generated, routes
from .client import WdsApiClient
from .exceptions import ApiActionException, NotAllowedVersionException
from .models import ApiActionResult, Headers, MsgpackModel
from .models_generated import AuthenticatePayload, AuthenticateResult, BooleanResult
from .transport import MasterDataInfo, SiriusApiClient

__all__ = [
    "WdsApiClient",
    "SiriusApiClient",
    "MasterDataInfo",
    "ApiActionException",
    "NotAllowedVersionException",
    "ApiActionResult",
    "MsgpackModel",
    "AuthenticatePayload",
    "AuthenticateResult",
    "BooleanResult",
    "Headers",
    "crypto",
    "decode",
    "routes",
    "models_generated",
]
