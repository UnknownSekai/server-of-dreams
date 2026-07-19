from fastapi import APIRouter, Response
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException

from helpers.assets import (
    bundle,
    catalog_br,
    catalog_hash,
    local_assets_enabled,
    notation,
    official_notation_url,
    official_url,
)

router = APIRouter(tags=["Assets"], include_in_schema=False)


def _octet(result) -> Response:
    body, content_md5 = result
    return Response(
        content=body,
        media_type="application/octet-stream",
        headers={"Content-MD5": content_md5},
    )


# Notation charts + music_config, served under /production/Notations/{music}/{file}.enc.
# This 3-segment path must be matched here -- otherwise redirect_slashes rewrites it and the
# client tries to AES-decrypt a redirect body (crash in SymmetricTransform). We hand back the
# raw encrypted bytes (local if downloaded, else a redirect to the real CDN).
@router.get("/production/Notations/{music_id}/{filename}", name="Assets_Notation")
async def asset_notation(music_id: str, filename: str) -> Response:
    if local_assets_enabled():
        local = notation(music_id, filename)
        if local is not None:
            return _octet(local)
    return RedirectResponse(official_notation_url(music_id, filename), status_code=302)


# Everything the client fetches from assets-e (redirected here). kind is
# 2d-assets|3d-assets|cri-assets, platform Android|iOS.
#   catalog_<ver>.json.br  -> brotli of the local catalog json
#   catalog_<ver>.hash     -> spookyhash-128 of the local catalog json
#   <group>/<name>.bundle  -> local file when local_assets is on, else a redirect to
#                             the official CDN (the mitm turns that 3xx into a passthrough)
@router.get(
    "/production/{kind}/{platform}/{version}/{filepath:path}", name="Assets_Production"
)
async def asset_production(
    kind: str, platform: str, version: str, filepath: str
) -> Response:
    if filepath.endswith(".json.br"):
        result = catalog_br(kind, platform)
    elif filepath.endswith(".hash"):
        result = catalog_hash(kind, platform)
    else:
        if local_assets_enabled():
            local = bundle(kind, platform, filepath)
            if local is not None:
                return _octet(local)
        return RedirectResponse(
            official_url(kind, platform, version, filepath), status_code=302
        )
    if result is None:
        raise HTTPException(status_code=404)
    return _octet(result)
