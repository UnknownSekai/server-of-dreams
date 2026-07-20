"""Download the current MasterMemory master-data blob and unpack it into per-table JSON.

    python -m scripts.download_masterdata                 # from the live API
    python -m scripts.download_masterdata --file some.db  # unpack a local blob

Registers a throwaway account on the official server, reads the MasterDataManifest for
the *current* master-data uri + SAS token (the publish timestamp changes on every update,
so a hardcoded one always 404s), downloads the blob, and decodes each table's rows through
its model into ``_data/masterdata/<Table>.json``. The ``/master-data`` route repacks them.
"""

import argparse
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from helpers.mastermemory import unpack  # noqa: E402
from helpers.msgpack import from_array  # noqa: E402
from models.master_data import TABLES  # noqa: E402
from scripts._sirius import MaintenanceError, master_data_manifest  # noqa: E402
from models import MasterDataManifest

OUT = Path(__file__).resolve().parent.parent / "_data" / "masterdata"


def _download_url(manifest: MasterDataManifest) -> str:
    uri, sas = manifest.uri or "", manifest.sas_token or ""
    if uri and sas:
        sep = "&" if "?" in uri else "?"
        return f"{uri}{sep}{sas.lstrip('?')}"
    return uri


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default=None, help="unpack a local blob instead")
    args = parser.parse_args()

    if args.file:
        db = Path(args.file).read_bytes()
        print(f"read {args.file} ({len(db)} bytes)")
    else:
        try:
            manifest: MasterDataManifest = master_data_manifest()
        except MaintenanceError:
            print("Server is in maintenance")
            return
        url = (
            "https://assets-e.wds-stellarium.com/master-data/production/"
            + _download_url(manifest)
        )
        print(
            f"master-data version {manifest.version} (publish {manifest.publish_timestamp})"
        )
        print(f"downloading {url}")
        req = urllib.request.Request(url, headers={"User-Agent": "server-of-dreams"})
        db = urllib.request.urlopen(req, timeout=120).read()
        print(f"downloaded {len(db)} bytes")

    tables = unpack(db)
    OUT.mkdir(parents=True, exist_ok=True)
    for name, rows in tables.items():
        model = TABLES.get(name)
        if model is None:
            continue
        keyed = [
            from_array(model.__name__, row).model_dump(mode="json", by_alias=True)
            for row in rows
        ]
        (OUT / f"{name}.json").write_text(
            json.dumps(keyed, ensure_ascii=False, indent=1), encoding="utf-8"
        )
    print(f"unpacked {len(tables)} tables -> {OUT}")


main()
