from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/Lessons", tags=["Lessons"])


# /api/Lessons/
@router.post("/", response_model=BooleanResult, name="Lessons_Start")
async def lessons_start(
    body: StartLessonPayload, characterBaseMasterId: str, liveMasterId: str
) -> BooleanResult:
    return BooleanResult()


# /api/Lessons/Finish
@router.post("/Finish", response_model=BooleanResult, name="Lessons_Finish")
async def lessons_finish(body: FinishLessonPayload) -> BooleanResult:
    return BooleanResult()
