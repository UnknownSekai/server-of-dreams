"""Download the MasterMemory master-data blob and unpack it into per-table JSON.

    python -m scripts.download_masterdata                 # from config's URL
    python -m scripts.download_masterdata --file some.db  # from a local blob

Rows are decoded through each table's model, so ``masterdata/<Table>.json`` is a
human-readable array of keyed objects. The ``/master-data`` route repacks them.
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
from helpers.config import config  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "masterdata"


MASTER_DATA_URL = "https://assets-e.wds-stellarium.com/master-data/production"


def source_url() -> str:
    ts = config["master_data_publish_timestamp"]
    return f"{MASTER_DATA_URL}/{_uri(ts)}"


def _uri(ts) -> str:
    import datetime

    day = datetime.datetime.fromtimestamp(int(ts), datetime.timezone.utc).strftime(
        "%Y-%m-%d"
    )
    return f"{day}/mastermemory_{ts}_{ts}.db"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=None, help="blob URL (default: from config)")
    parser.add_argument("--file", default=None, help="unpack a local blob instead")
    args = parser.parse_args()

    if args.file:
        db = Path(args.file).read_bytes()
        print(f"read {args.file} ({len(db)} bytes)")
    else:
        url = args.url or source_url()
        print(f"downloading {url}")
        req = urllib.request.Request(url, headers={"User-Agent": "server-of-dreams"})
        db = urllib.request.urlopen(req, timeout=120).read()
        print(f"downloaded {len(db)} bytes")

    tables = unpack(db)
    OUT.mkdir(exist_ok=True)
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
