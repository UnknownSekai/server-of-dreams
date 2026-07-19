from typing import Optional

from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(tags=["KmsGeneralPayment"])


# /api/Payments/process/appstore
@router.post(
    "/api/Payments/process/appstore", name="KmsGeneralPayment_ProcessAppStorePayment"
)
async def kms_general_payment_process_app_store_payment(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, RegisterAppStorePaymentPayload)
    return respond(ProcessPaymentResult())


# /api/Payments/process/googleplay
@router.post(
    "/api/Payments/process/googleplay",
    name="KmsGeneralPayment_ProcessGooglePlayPayment",
)
async def kms_general_payment_process_google_play_payment(request: Request):
    app: YumeApp = request.app
    payload = await read_request(request, RegisterGooglePlayPaymentPayload)
    return respond(ProcessPaymentResult())
