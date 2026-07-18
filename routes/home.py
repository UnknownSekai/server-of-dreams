from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/Home", tags=["Home"])


# /api/Home/CheckEexternalPayment
@router.post(
    "/CheckEexternalPayment",
    response_model=EexternalPaymentResult,
    name="Home_CheckEexternalPayment",
)
async def home_check_eexternal_payment() -> EexternalPaymentResult:
    return EexternalPaymentResult()


# /api/Home/CheckReceiveLoginBonus
@router.post(
    "/CheckReceiveLoginBonus",
    response_model=list[LoginBonusResult],
    name="Home_CheckReceiveLoginBonus",
)
async def home_check_receive_login_bonus() -> list[LoginBonusResult]:
    return []


# /api/Home/GetMultiLiveRestrictionNotification
@router.post(
    "/GetMultiLiveRestrictionNotification",
    response_model=BooleanResult,
    name="Home_GetMultiLiveRestrictionNotification",
)
async def home_get_multi_live_restriction_notification() -> BooleanResult:
    return BooleanResult()


# /api/Home/GetNotificationsAsync
@router.post(
    "/GetNotificationsAsync",
    response_model=list[NotificationResult],
    name="Home_GetNotifications",
)
async def home_get_notifications() -> list[NotificationResult]:
    return []


# /api/Home/GetNotificationsInTitleAsync
@router.get(
    "/GetNotificationsInTitleAsync",
    response_model=list[NotificationResult],
    name="Home_GetNotificationsAnonymous",
)
async def home_get_notifications_anonymous() -> list[NotificationResult]:
    return []


# /api/Home/UpdateNotificationReadTime
@router.post(
    "/UpdateNotificationReadTime",
    response_model=BooleanResult,
    name="Home_UpdateNotificationReadTime",
)
async def home_update_notification_read_time(
    body: ReadNotificationPayload,
) -> BooleanResult:
    return BooleanResult()
