import datetime
from typing import Optional

from helpers.cache import cache
from helpers.config import config
from helpers.mastermemory import pack
from helpers.msgpack import to_wire
from models import MasterDataManifest
from models.master_data import MasterData

_db_cache: dict = {"bytes": None}


def _publish_timestamp() -> int:
    return int(config["master_data_publish_timestamp"])


def master_data_manifest() -> MasterDataManifest:
    ts = _publish_timestamp()
    version = f"{ts}_{ts}"
    day = datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).strftime(
        "%Y-%m-%d"
    )
    return MasterDataManifest(
        uri=f"{day}/mastermemory_{version}.db",
        sas_token="",  # Azure blob SAS; we serve the blob ourselves, so it's unused
        version=version,
        publish_timestamp=ts,
    )


def master_data_db() -> Optional[bytes]:
    """The MasterMemory blob repacked from the cached master-data models (memoized)."""
    if _db_cache["bytes"] is None:
        tables = {
            info.alias: [to_wire(m) for m in getattr(cache, field)]
            for field, info in MasterData.model_fields.items()
        }
        if any(tables.values()):
            _db_cache["bytes"] = pack(tables)
    return _db_cache["bytes"]
