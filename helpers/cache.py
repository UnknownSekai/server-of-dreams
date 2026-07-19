"""In-memory master data, loaded from ``masterdata/*.json`` at startup.

    from helpers.cache import cache
    cache.accessory_master        # list[AccessoryMaster]  (typed)
    cache.music_master            # list[MusicMaster]

``cache`` is a :class:`~models.master_data.MasterData` instance (fields are the
snake_case table names). Empty until ``load_master_data()`` runs on app startup.
"""

import json
from pathlib import Path

from models.master_data import MasterData, TABLES

_DIR = Path(__file__).resolve().parent.parent / "masterdata"

cache = MasterData()


def load_master_data() -> None:
    data = {}
    for name in TABLES:
        path = _DIR / f"{name}.json"
        if path.exists():
            data[name] = json.loads(path.read_text(encoding="utf-8"))
    loaded = MasterData.model_validate(data)
    cache.__dict__.update(loaded.__dict__)
