from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/Payments", tags=["Payments"])


# /api/Payments/process/appstore
@router.post("/process/appstore", name="KmsGeneralPayment_ProcessAppStorePayment")
async def kms_general_payment_process_app_store_payment(request: Request):
    payload = await read_request(request, "RegisterAppStorePaymentPayload")
    return respond(ProcessPaymentResult())


# /api/Payments/process/googleplay
@router.post("/process/googleplay", name="KmsGeneralPayment_ProcessGooglePlayPayment")
async def kms_general_payment_process_google_play_payment(request: Request):
    payload = await read_request(request, "RegisterGooglePlayPaymentPayload")
    return respond(ProcessPaymentResult())
