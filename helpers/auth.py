import datetime
import secrets
import time
from typing import Optional

import jwt

from db.account import (
    add_hash_user_id,
    create_account,
    get_account_by_id,
    next_user_id,
    update_account_token,
)
from db.defaults import create_default_user_data
from helpers.config import config
from helpers.user_hash import hash_id
from models import AccountRegistResult, AuthenticateResult, LoginResult

_JWT_ISS = "server-of-dreams"
_JWT_AUD = "github.com/UnknownSekai/server-of-dreams"
_TOKEN_TTL = 3600  # register token
_SESSION_TTL = 86400  # authenticated session token
_JST = datetime.timezone(datetime.timedelta(hours=9))


def _secret() -> str:
    return str(config["jwt_secret"])


def _login_day() -> str:
    now = datetime.datetime.now(_JST)
    day = now if now.hour >= 5 else now - datetime.timedelta(days=1)
    return day.strftime("%m/%d/%Y 05:00:00")


def make_jwt(user_id: int) -> str:
    now = int(time.time())
    return jwt.encode(
        {
            "uid": str(user_id),
            "nbf": now,
            "exp": now + _TOKEN_TTL,
            "iat": now,
            "iss": _JWT_ISS,
            "aud": _JWT_AUD,
        },
        _secret(),
        algorithm="HS256",
    )


def make_session_jwt(user_id: int, platform: str) -> str:
    now = int(time.time())
    return jwt.encode(
        {
            "uid": str(user_id),
            "lc": "1",
            "pf": platform,
            "gv": platform,
            "ld": _login_day(),
            "nbf": now,
            "exp": now + _SESSION_TTL,
            "iat": now,
            "iss": _JWT_ISS,
            "aud": _JWT_AUD,
        },
        _secret(),
        algorithm="HS256",
    )


def decode_jwt(token: str, verify_exp: bool = True) -> Optional[int]:
    try:
        claims = jwt.decode(
            token,
            _secret(),
            algorithms=["HS256"],
            audience=_JWT_AUD,
            issuer=_JWT_ISS,
            options={"verify_exp": verify_exp},
        )
        return int(claims["uid"])
    except Exception:
        return None


async def _new_user_id(conn) -> int:
    row = await conn.fetchrow(next_user_id())
    if row is None:
        raise RuntimeError("could not allocate a user id")
    return row.value


async def register(payload, app) -> AccountRegistResult:
    name = getattr(payload, "name", "") or ""
    async with app.acquire_db() as conn, conn.transaction():
        user_id = await _new_user_id(conn)
        token = make_jwt(user_id)
        now = int(time.time())
        # lastLoginAt=0 marks "never logged in" so the first Login can emit the full present
        await conn.execute(
            create_account(user_id, secrets.token_urlsafe(24), "Android", now, 0)
        )
        await conn.execute(add_hash_user_id(hash_id(user_id), user_id))
        await conn.execute(update_account_token(user_id, token))
        await create_default_user_data(conn, user_id, name)
    return AccountRegistResult(token=token, error_type=0)


async def authenticate(payload, app) -> AuthenticateResult:
    # the login_token is a token we issued earlier; accept it even if expired.
    user_id = decode_jwt(getattr(payload, "login_token", "") or "", verify_exp=False)
    if user_id is None:
        return AuthenticateResult(token="", ban_level=0, warned_until=None)
    game_version = getattr(payload, "game_version", None)
    platform = game_version.name if game_version is not None else "Unknown"
    token = make_session_jwt(user_id, platform)
    ban_level = 0
    async with app.acquire_db() as conn:
        account = await conn.fetchrow(get_account_by_id(user_id))
        if account is not None:
            ban_level = account.banLevel
        await conn.execute(update_account_token(user_id, token))
    return AuthenticateResult(token=token, ban_level=ban_level, warned_until=None)


def login(payload=None) -> LoginResult:
    return LoginResult(
        invalided_star_passes=[],
        login_pass_notification=0,
        is_approaching_login_pass_invalided=False,
        invalided_item_master_ids=[],
        approaching_item_master_ids=[],
        story_event_point_exchange_result=[],
        invalided_buff_item_master_ids=[],
    )
