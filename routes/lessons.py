from fastapi import APIRouter, Request

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(prefix="/api/Lessons", tags=["Lessons"])


# /api/Lessons/
@router.post("/", name="Lessons_Start")
async def lessons_start(request: Request):
    payload = await read_request(request, "StartLessonPayload")
    return respond(BooleanResult())


# /api/Lessons/Finish
@router.post("/Finish", name="Lessons_Finish")
async def lessons_finish(request: Request):
    payload = await read_request(request, "FinishLessonPayload")
    return respond(BooleanResult())
