from fastapi import APIRouter, Request

from helpers.game_state import (
    Rejected,
    costume_owned,
    master,
    mission_progress,
    transaction,
)
from helpers.msgpack import read_request, respond
from models import *

router = APIRouter(tags=["Possessions"])


async def _toggle_favorite_stamp(request: Request, ident: int, add: bool):
    try:
        async with transaction(request) as s:
            row = await s.one("Stamp")
            m = master("stamp_master", ident)
            if (
                not row
                or not m
                or (not m.is_default and ident not in (row["stampMasterIds"] or []))
            ):
                raise Rejected()
            favorites = list(row["favoriteStampMasterIds"] or [])
            if add:
                if ident not in favorites:
                    favorites.append(ident)
                    await mission_progress(s, 21, create=True)
            else:
                favorites = [v for v in favorites if v != ident]
            await s.update("Stamp", row, favoriteStampMasterIds=favorites)
        return respond(BooleanResult(is_success=True), present=s.present())
    except Rejected:
        return respond(BooleanResult())


# /api/Possessions/AddFavoriteStamp/{mStampId}
@router.post(
    "/api/Possessions/AddFavoriteStamp/{mStampId}", name="Possessions_AddFavoriteStamp"
)
async def possessions_add_favorite_stamp(request: Request, mStampId: int):
    return await _toggle_favorite_stamp(request, mStampId, add=True)


# /api/Possessions/RemoveFavoriteStamp/{mStampId}
@router.post(
    "/api/Possessions/RemoveFavoriteStamp/{mStampId}",
    name="Possessions_RemoveFavoriteStamp",
)
async def possessions_remove_favorite_stamp(request: Request, mStampId: int):
    return await _toggle_favorite_stamp(request, mStampId, add=False)


# /api/Possessions/SetFavorite
@router.post("/api/Possessions/SetFavorite", name="Possessions_BulkSetCostumeFavorite")
async def possessions_bulk_set_costume_favorite(request: Request):
    try:
        p = await read_request(request, CostumeFavoritePayload)
        if p is None:
            raise Rejected()
        base, ident = p.character_base_master_id, p.costume_master_id
        async with transaction(request) as s:
            await costume_owned(s, base, ident)
            row = await s.one("FavoriteCostume", characterBaseMasterId=base)
            favorites = list(row["favoriteCostumeMasterIds"] or []) if row else []
            if p.set_favorite and ident not in favorites:
                favorites.append(ident)
            if not p.set_favorite:
                favorites = [v for v in favorites if v != ident]
            if row:
                await s.update(
                    "FavoriteCostume", row, favoriteCostumeMasterIds=favorites
                )
            else:
                await s.insert(
                    "FavoriteCostume",
                    characterBaseMasterId=base,
                    favoriteCostumeMasterIds=favorites,
                )
        return respond(BooleanResult(is_success=True), present=s.present())
    except Rejected:
        return respond(BooleanResult())


# /api/Possessions/SortFavoriteStamps
@router.post(
    "/api/Possessions/SortFavoriteStamps", name="Possessions_SortFavoriteStamps"
)
async def possessions_sort_favorite_stamps(request: Request):
    try:
        p = await read_request(request, FavoriteStampOrderPayload)
        if p is None:
            raise Rejected()
        order = [int(s) for s in (p.stamp_master_ids or [])]
        async with transaction(request) as s:
            row = await s.one("Stamp")
            if not row:
                raise Rejected()
            # a reorder keeps exactly the current favorites, only their sequence changes
            current = set(row["favoriteStampMasterIds"] or [])
            await s.update(
                "Stamp",
                row,
                favoriteStampMasterIds=[i for i in order if i in current],
            )
        return respond(BooleanResult(is_success=True), present=s.present())
    except Rejected:
        return respond(BooleanResult())
