"""Download every asset bundle for the game into ``assets/`` (Android + iOS).

    python -m scripts.download_asset_catalogs
    python -m scripts.download_all_assets --dry-run # do a check of work first
    python -m scripts.download_all_assets # actually do the download

Each catalog's ``m_InternalIds`` encodes bundles as ``<prefixIndex>#/<name>`` which
resolve (via ``m_InternalIdPrefixes``) to ``http://<kind>/<platform>/<group>/<name>``.
The real file lives at ``<asset_url>/<kind>/<platform>/<version>/<group>/<name>`` and
is saved to ``assets/<kind>/<platform>/<group>/<name>``. Existing files are skipped,
so re-running resumes. This is the entire game -- expect many GB.
"""

import argparse
import json
import re
import shutil
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from helpers.config import config  # noqa: E402

ASSETS = Path(__file__).resolve().parent.parent / "assets"
ASSET_URL = "https://assets-e.wds-stellarium.com/production"
KINDS = ("2d-assets", "3d-assets", "cri-assets")
PLATFORMS = ("Android", "iOS")
_REF = re.compile(r"^(\d+)#(.*)$")


def bundle_rel_paths(catalog_path: Path) -> list:
    """Distinct ``<group>/<name>.bundle`` paths (relative to the version dir)."""
    data = json.loads(catalog_path.read_text(encoding="utf-8"))
    prefixes = data["m_InternalIdPrefixes"]
    out, seen = [], set()
    for iid in data["m_InternalIds"]:
        if not iid.endswith(".bundle"):
            continue
        m = _REF.match(iid)
        resolved = (
            prefixes[int(m.group(1))] + m.group(2)
            if m and int(m.group(1)) < len(prefixes)
            else iid
        )
        # http://<kind>/<platform>/<group>/<name> -> <group>/<name>
        tail = resolved.split("://", 1)[-1].split("/", 2)
        rel = tail[2] if len(tail) == 3 else resolved
        if rel not in seen:
            seen.add(rel)
            out.append(rel)
    return out


def _download(url: str, dest: Path) -> str:
    if dest.exists():
        return "skip"
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".part")
    req = urllib.request.Request(url, headers={"User-Agent": "server-of-dreams"})
    with urllib.request.urlopen(req, timeout=120) as r, open(tmp, "wb") as f:
        shutil.copyfileobj(r, f)
    tmp.replace(dest)  # atomic: a killed download never leaves a "complete" file
    return "ok"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="count bundles only")
    parser.add_argument("--workers", type=int, default=16, help="parallel downloads")
    parser.add_argument("--limit", type=int, default=0, help="max bundles per catalog")
    parser.add_argument("--kind", choices=KINDS, help="only this asset kind")
    parser.add_argument("--platform", choices=PLATFORMS, help="only this platform")
    args = parser.parse_args()

    version = str(config["asset_version"])
    kinds = (args.kind,) if args.kind else KINDS
    platforms = (args.platform,) if args.platform else PLATFORMS

    grand_total = 0
    for kind in kinds:
        for platform in platforms:
            root = ASSETS / kind / platform.lower()
            catalog = root / "catalog.json"
            if not catalog.is_file():
                print(f"{kind}/{platform}: no catalog (run download_asset_catalogs)")
                continue
            rels = bundle_rel_paths(catalog)
            if args.limit:
                rels = rels[: args.limit]
            grand_total += len(rels)
            print(f"{kind}/{platform}: {len(rels)} bundles")
            if args.dry_run:
                continue

            ok = skip = err = done = 0
            with ThreadPoolExecutor(max_workers=args.workers) as pool:
                futures = {
                    pool.submit(
                        _download,
                        f"{ASSET_URL}/{kind}/{platform}/{version}/{rel}",
                        root / rel,
                    ): rel
                    for rel in rels
                }
                for fut in as_completed(futures):
                    done += 1
                    try:
                        res = fut.result()
                        ok += res == "ok"
                        skip += res == "skip"
                    except urllib.error.HTTPError as e:
                        err += 1
                        print(f"  ! {futures[fut]} ({e.code})")
                    except Exception as e:  # noqa: BLE001
                        err += 1
                        print(f"  ! {futures[fut]} ({type(e).__name__})")
                    if done % 200 == 0 or done == len(rels):
                        print(f"  {done}/{len(rels)} ok={ok} skip={skip} err={err}")

    print(f"total bundles: {grand_total}")


main()
