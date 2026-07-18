from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/Payments", tags=["Payments"])


# /api/Payments/process/appstore
@router.post(
    "/process/appstore",
    response_model=ProcessPaymentResult,
    name="KmsGeneralPayment_ProcessAppStorePayment",
)
async def kms_general_payment_process_app_store_payment(
    body: RegisterAppStorePaymentPayload,
) -> ProcessPaymentResult:
    return ProcessPaymentResult()


# /api/Payments/process/googleplay
@router.post(
    "/process/googleplay",
    response_model=ProcessPaymentResult,
    name="KmsGeneralPayment_ProcessGooglePlayPayment",
)
async def kms_general_payment_process_google_play_payment(
    body: RegisterGooglePlayPaymentPayload,
) -> ProcessPaymentResult:
    return ProcessPaymentResult()
