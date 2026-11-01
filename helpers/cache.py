"""In-memory master data, loaded from ``_data/masterdata/*.json`` at startup.

    from helpers.cache import cache
    cache.accessory_master        # list[AccessoryMaster]  (typed)
    cache.music_master            # list[MusicMaster]

``cache`` is a :class:`~models.master_data.MasterData` instance (fields are the
snake_case table names). Empty until ``load_master_data()`` runs on app startup.
"""

import datetime
import json
from pathlib import Path

from models.master_data import MasterData, TABLES

_DIR = Path(__file__).resolve().parent.parent / "_data" / "masterdata"

cache = MasterData()

# The service ended 2026-09-29; content meant to run "until the end" carries an end date
# pinned to that moment (23:00 JST, and the 14:00 JST / 05:00 UTC daily-reset representation).
# Left as-is it expires everything post-shutdown -- shops empty out, schedules and Anthology
# content drop off, and the performance menu throws error 81. We lift those boundary end dates
# to the game's own permanent sentinel (2100-01-01) so that content stays available, exactly
# as if the service were still running. Genuinely time-limited past events keep their own
# earlier end dates and stay expired. Applied to the cache at load time, so both the server's
# own logic and the master-data blob it repacks for the client see the extended dates.
_SERVICE_END_BOUNDARIES = {1790658000, 1790690400}
_PERMANENT_END = (
    "2100-01-01T00:00:00+00:00"  # 4102444800; the game's permanent-chart value
)
_EPOCH_UTC = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)


def _is_service_end_boundary(value: str) -> bool:
    try:
        dt = datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    return int((dt - _EPOCH_UTC).total_seconds()) in _SERVICE_END_BOUNDARIES


def _extend_service_end_dates() -> int:
    """Lift every end date sitting exactly on the service-end boundary to the permanent
    sentinel, recursing through nested master models. Returns how many were moved."""
    moved = 0

    def walk(obj) -> None:
        nonlocal moved
        if isinstance(obj, list):
            for item in obj:
                walk(item)
        elif hasattr(type(obj), "model_fields"):
            for field, value in list(obj.__dict__.items()):
                if isinstance(value, str):
                    # the boundary-value test is the real guard; the name just narrows it
                    if "end" in field and _is_service_end_boundary(value):
                        setattr(obj, field, _PERMANENT_END)
                        moved += 1
                elif isinstance(value, list) or hasattr(type(value), "model_fields"):
                    walk(value)

    for field in MasterData.model_fields:
        walk(getattr(cache, field))
    return moved


def load_master_data() -> None:
    data = {}
    for name in TABLES:
        path = _DIR / f"{name}.json"
        if path.exists():
            data[name] = json.loads(path.read_text(encoding="utf-8"))
    loaded = MasterData.model_validate(data)
    cache.__dict__.update(loaded.__dict__)
    _extend_service_end_dates()
