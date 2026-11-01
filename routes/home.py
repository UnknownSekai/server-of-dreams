import datetime
from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(tags=["Home"])


# /api/Home/CheckEexternalPayment
@router.post("/api/Home/CheckEexternalPayment", name="Home_CheckEexternalPayment")
async def home_check_eexternal_payment(request: Request):
    app: YumeApp = request.app
    # ApiActionResult - single item not list style
    return respond(EexternalPaymentResult())


# /api/Home/CheckReceiveLoginBonus
@router.post("/api/Home/CheckReceiveLoginBonus", name="Home_CheckReceiveLoginBonus")
async def home_check_receive_login_bonus(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    # the client's login-bonus flow takes an AsyncLock (SemaphoreSlim) and only releases it after
    # it has processed at least one structurally-complete LoginBonusResult. an empty array is a
    # valid array but leaves that lock held forever -> silent deadlock on Main scene init (white
    # screen + logo, UnityMain stuck in futex_wait, no further requests). return one complete
    # result so the flow completes. real rewards still need LoginBonusMaster/LoginBonusDetailMaster
    # (absent from our unpacked masterdata), so nothing is granted yet -- received_things/details
    # stay empty.
    now = (
        datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
    )
    return respond(
        [
            LoginBonusResult(
                login_bonus_id=1,
                current_login_count=1,
                received_things=[],
                title="ログインボーナス",
                type=LoginBonusTypes.Normal,
                start_date=now,
                message_template="ログインボーナス {0}日目",
                total_days=7,
                is_loop=True,
                order=1,
                details=[],
                layout_type=LoginBonusLayoutTypes.Normal,
            )
        ]
    )


# /api/Home/GetMultiLiveRestrictionNotification
@router.post(
    "/api/Home/GetMultiLiveRestrictionNotification",
    name="Home_GetMultiLiveRestrictionNotification",
)
async def home_get_multi_live_restriction_notification(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(BooleanResult())


# /api/Home/GetNotificationsAsync/{mNotificationId}
@router.post(
    "/api/Home/GetNotificationsAsync/{mNotificationId}",
    name="Home_GetNotificationContent",
)
async def home_get_notification_content(request: Request, mNotificationId: int):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(NotificationContentResult())


# /api/Home/GetNotificationsInTitleAsync/{mNotificationId}
@router.get(
    "/api/Home/GetNotificationsInTitleAsync/{mNotificationId}",
    name="Home_GetNotificationContentAnonymous",
)
async def home_get_notification_content_anonymous(
    request: Request, mNotificationId: int
):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(NotificationContentResult())


# /api/Home/GetNotificationsAsync
@router.post("/api/Home/GetNotificationsAsync", name="Home_GetNotifications")
async def home_get_notifications(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    # ApiActionResult<NotificationResult[]> -- empty for now
    # return respond([NotificationResult()])
    return respond([])


# /api/Home/GetNotificationsInTitleAsync
@router.get(
    "/api/Home/GetNotificationsInTitleAsync", name="Home_GetNotificationsAnonymous"
)
async def home_get_notifications_anonymous(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    # ApiActionResult<NotificationResult[]> -- empty for now
    # return respond([NotificationResult()])
    return respond([])


# /api/Home/UpdateNotificationReadTime
@router.post(
    "/api/Home/UpdateNotificationReadTime", name="Home_UpdateNotificationReadTime"
)
async def home_update_notification_read_time(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, ReadNotificationPayload)
    return respond(BooleanResult())
