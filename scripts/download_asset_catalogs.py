"""Download and decompress the Unity Addressables asset catalogs.

    python -m scripts.download_asset_catalogs

Each ``catalog_<ver>.json.br`` is a Brotli-compressed Addressables catalog. This
fetches every kind/platform pair and writes the decompressed catalog to
``_data/assets/<kind>/<platform>/catalog.json``.
"""

import sys
import urllib.error
import urllib.request
from pathlib import Path

import brotli

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts._sirius import MaintenanceError, environment  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "_data" / "assets"
ASSET_URL = "https://assets-e.wds-stellarium.com/production"
KINDS = ("2d-assets", "3d-assets", "cri-assets")
PLATFORMS = ("Android", "iOS")


def catalog_url(kind: str, platform: str, version: str) -> str:
    return f"{ASSET_URL}/{kind}/{platform}/{version}/catalog_{version}.json.br"


def main() -> None:
    try:
        version = str(environment().asset_version)
    except MaintenanceError:
        print("Server is in maintenance")
        return
    print(f"asset version {version}")
    ok = 0
    for kind in KINDS:
        for platform in PLATFORMS:
            url = catalog_url(kind, platform, version)
            print(f"downloading {url}")
            try:
                req = urllib.request.Request(
                    url, headers={"User-Agent": "server-of-dreams"}
                )
                data = urllib.request.urlopen(req, timeout=120).read()
            except urllib.error.HTTPError as e:
                print(f"  skipped ({e.code} {e.reason})")
                continue
            catalog = brotli.decompress(data)
            dest = OUT / kind / platform.lower() / "catalog.json"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(catalog)
            print(
                f"  {len(data)} br -> {len(catalog)} json -> {dest.relative_to(OUT.parent)}"
            )
            ok += 1
    print(f"wrote {ok} catalogs -> {OUT}")


main()
