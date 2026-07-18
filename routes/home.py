from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/Home", tags=["Home"])


# /api/Home/CheckEexternalPayment
@router.post("/CheckEexternalPayment", name="Home_CheckEexternalPayment")
async def home_check_eexternal_payment(request: Request):
    return respond(EexternalPaymentResult())


# /api/Home/CheckReceiveLoginBonus
@router.post("/CheckReceiveLoginBonus", name="Home_CheckReceiveLoginBonus")
async def home_check_receive_login_bonus(request: Request):
    return respond([])


# /api/Home/GetMultiLiveRestrictionNotification
@router.post(
    "/GetMultiLiveRestrictionNotification",
    name="Home_GetMultiLiveRestrictionNotification",
)
async def home_get_multi_live_restriction_notification(request: Request):
    return respond(BooleanResult())


# /api/Home/GetNotificationsAsync
@router.post("/GetNotificationsAsync", name="Home_GetNotifications")
async def home_get_notifications(request: Request):
    return respond([])


# /api/Home/GetNotificationsInTitleAsync
@router.get("/GetNotificationsInTitleAsync", name="Home_GetNotificationsAnonymous")
async def home_get_notifications_anonymous(request: Request):
    return respond([])


# /api/Home/UpdateNotificationReadTime
@router.post("/UpdateNotificationReadTime", name="Home_UpdateNotificationReadTime")
async def home_update_notification_read_time(request: Request):
    payload = await read_request(request, "ReadNotificationPayload")
    return respond(BooleanResult())
