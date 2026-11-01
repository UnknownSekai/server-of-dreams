"""Download every game asset from the published release into ``_data/assets/``.

    python -m scripts.download_all_assets --dry-run                        # list zips + destinations
    python -m scripts.download_all_assets                                  # download + extract everything
    python -m scripts.download_all_assets --only notations scenes static-assets
    python -m scripts.download_all_assets --only 2d-assets --platform android

The live CDN (assets-e.wds-stellarium.com) is dead (EOS), so rather than crawling it
bundle-by-bundle we pull the pre-packaged release zips and unpack each into place:

    <kind>-<platform>[-N].zip -> _data/assets/<kind>/<platform>/   (catalog.json + *.bundle)
    notations.zip             -> _data/assets/Notations/
    scenes.zip                -> _data/assets/scenes/
    static-assets.zip         -> _data/assets/static-assets/

The masterdata zip in the same release is skipped -- that belongs to
``scripts.download_masterdata``. Already-extracted files are skipped, so a re-run resumes.
This is the entire game -- expect many tens of GB.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from typing import NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS = PROJECT_ROOT / "_data" / "assets"
ZIP_CACHE = ASSETS / ".zips"

REPO = "Ryota537/asset-of-dreams"
TAG = "1.96.0-7"
UA = "server-of-dreams"

KINDS = ("2d-assets", "3d-assets", "cri-assets")
PLATFORMS = ("android", "ios")
# release base name -> destination dir name under _data/assets/
EXTRA_DESTS = {
    "notations": "Notations",
    "scenes": "scenes",
    "static-assets": "static-assets",
}
CATEGORIES = KINDS + tuple(EXTRA_DESTS)

# "<base>.zip" or "<base>-<part>.zip" (multi-part release zips add a "-N" split suffix)
_SPLIT = re.compile(r"^(?P<base>.+?)(?:-(?P<part>\d+))?\.zip$")


class Zip(NamedTuple):
    name: str
    url: str
    size: int
    dest: Path


def resolve(name: str) -> tuple[str, Path] | None:
    """(category, destination dir) a release zip unpacks into, or None to skip it."""
    m = _SPLIT.match(name)
    if not m:
        return None
    base = m.group("base")
    if base in EXTRA_DESTS:
        return base, ASSETS / EXTRA_DESTS[base]
    for kind in KINDS:
        platform = base[len(kind) + 1 :]
        if base.startswith(kind + "-") and platform in PLATFORMS:
            return kind, ASSETS / kind / platform
    return None


def release_assets(tag: str) -> list[dict]:
    url = f"https://api.github.com/repos/{REPO}/releases/tags/{tag}"
    headers = {"User-Agent": UA, "Accept": "application/vnd.github+json"}
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8")).get("assets", [])


def _download(url: str, dest: Path, size: int) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=300) as r, open(dest, "wb") as f:
        done = 0
        while chunk := r.read(1 << 20):
            f.write(chunk)
            done += len(chunk)
            pct = f" ({done * 100 // size}%)" if size else ""
            print(f"\r  downloading {done / 1e6:7.0f} MB{pct}", end="", flush=True)
    print()


def _extract(zip_path: Path, dest: Path) -> tuple[int, int]:
    """Unpack every file into ``dest``, skipping ones already present at the same size."""
    dest.mkdir(parents=True, exist_ok=True)
    root = dest.resolve()
    ok = skip = 0
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            target = (dest / info.filename).resolve()
            if target != root and root not in target.parents:  # guard against zip-slip
                print(f"  ! unsafe path skipped: {info.filename}")
                continue
            if target.exists() and target.stat().st_size == info.file_size:
                skip += 1
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info) as src, open(target, "wb") as out:
                shutil.copyfileobj(src, out)
            ok += 1
    return ok, skip


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", default=TAG, help="release tag to pull from")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="list zips + destinations, download nothing",
    )
    parser.add_argument(
        "--only", nargs="+", choices=CATEGORIES, help="limit to these categories"
    )
    parser.add_argument(
        "--platform", choices=PLATFORMS, help="limit bundle downloads to one platform"
    )
    parser.add_argument(
        "--keep-zips",
        action="store_true",
        help="keep downloaded zips instead of deleting them",
    )
    args = parser.parse_args()

    try:
        assets = release_assets(args.tag)
    except urllib.error.HTTPError as e:
        print(f"failed to fetch release {args.tag}: {e.code} {e.reason}")
        return

    plan: list[Zip] = []
    for a in assets:
        name = a["name"]
        resolved = resolve(name)
        if resolved is None:
            print(f"skipping {name} (not an asset zip)")
            continue
        category, dest = resolved
        if args.only and category not in args.only:
            continue
        if args.platform and category in KINDS and dest.name != args.platform:
            continue
        plan.append(Zip(name, a["browser_download_url"], int(a["size"]), dest))

    total = sum(z.size for z in plan)
    print(f"\nrelease {args.tag}: {len(plan)} zip(s), {total / 1e9:.1f} GB to download")
    for z in plan:
        print(
            f"  {z.name:34} {z.size / 1e6:8.1f} MB -> {z.dest.relative_to(PROJECT_ROOT)}"
        )
    if args.dry_run or not plan:
        return

    for z in plan:
        print(f"\n{z.name} -> {z.dest.relative_to(PROJECT_ROOT)}")
        zip_path = ZIP_CACHE / z.name
        if zip_path.exists() and zip_path.stat().st_size == z.size:
            print("  (already downloaded)")
        else:
            part = zip_path.with_name(z.name + ".part")
            _download(z.url, part, z.size)
            if part.stat().st_size != z.size:
                print(f"  ! size mismatch ({part.stat().st_size} != {z.size}); skipped")
                part.unlink(missing_ok=True)
                continue
            part.replace(zip_path)  # atomic: a killed download never looks complete
        ok, skip = _extract(zip_path, z.dest)
        print(f"  extracted {ok} file(s), skipped {skip} already present")
        if not args.keep_zips:
            zip_path.unlink(missing_ok=True)

    if not args.keep_zips and ZIP_CACHE.is_dir():
        shutil.rmtree(ZIP_CACHE, ignore_errors=True)
    print("\ndone")


main()
