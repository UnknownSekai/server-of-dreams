import time
from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from db.account import get_account_by_id, update_last_login
from helpers.daily import refresh_daily_limits
from helpers.msgpack import read_request, respond
from helpers.auth import login
from helpers.user_data import build_present, current_user_id
from models import *

router = APIRouter(tags=["Login"])


# /api/Login
@router.post("/api/Login", name="Login_Login")
async def login_login(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, LoginPayload)
    user_id = current_user_id(request)
    await refresh_daily_limits(app, user_id)
    async with app.acquire_db() as conn:
        account = await conn.fetchrow(get_account_by_id(user_id))
        first_login = account is not None and account.lastLoginAt == 0
        await conn.execute(update_last_login(user_id, int(time.time())))
    # first login surfaces the whole freshly-created account; later logins only touch User
    if first_login:
        present = await build_present(
            app, user_id, "Inbox", "FriendInvitation", "MissionPass", "User"
        )
    else:
        present = await build_present(app, user_id, "User")
    return respond(login(payload), present=present)
