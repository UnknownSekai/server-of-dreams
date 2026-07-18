from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import raw_response, read_request, respond
from models import *

router = APIRouter(tags=["Home"])


# /api/Home/CheckEexternalPayment
@router.post("/api/Home/CheckEexternalPayment", name="Home_CheckEexternalPayment")
async def home_check_eexternal_payment(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond(EexternalPaymentResult())


# /api/Home/CheckReceiveLoginBonus
@router.post("/api/Home/CheckReceiveLoginBonus", name="Home_CheckReceiveLoginBonus")
async def home_check_receive_login_bonus(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])


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
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(NotificationContentResult())


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
    # does not use common response (ParseWithoutCommonResponse APIClient)
    return raw_response(NotificationContentResult())


# /api/Home/GetNotificationsAsync
@router.post("/api/Home/GetNotificationsAsync", name="Home_GetNotifications")
async def home_get_notifications(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])


# /api/Home/GetNotificationsInTitleAsync
@router.get(
    "/api/Home/GetNotificationsInTitleAsync", name="Home_GetNotificationsAnonymous"
)
async def home_get_notifications_anonymous(request: Request):
    app: YumeApp = request.app
    payload = {}  # no payload
    return respond([])


# /api/Home/UpdateNotificationReadTime
@router.post(
    "/api/Home/UpdateNotificationReadTime", name="Home_UpdateNotificationReadTime"
)
async def home_update_notification_read_time(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, "ReadNotificationPayload")
    return respond(BooleanResult())
