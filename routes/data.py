from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from models import *

router = APIRouter(prefix="/api/data", tags=["data"])


# /api/data/master
@router.get("/master", response_model=MasterDataManifest, name="Data_GetMasterData")
async def data_get_master_data() -> MasterDataManifest:
    return MasterDataManifest()


# /api/data/user
@router.get("/user", response_model=list[Any], name="Data_GetUserData")
async def data_get_user_data() -> list[Any]:
    return []
