"""Daily-limit reset at 05:00 JST. When a data-fetch happens after the day's reset
boundary, each daily allowance is topped back up to its max and lastRefreshedAt advances.
"""

import datetime
import time

from db.user import get_daily_limits, update_daily_limit

_JST = datetime.timezone(datetime.timedelta(hours=9))
_MICRO = 1_000_000

# Allowances restored to these maxima at 05:00 JST.
# TODO: the rank-1 capture shows 0 for all three -- they appear to unlock through
# progression, and the real maxima aren't in masterdata or the dump. Fill in the real
# (likely rank-scaled) values; left at 0 for now so the reset is a no-op.
DAILY_MAX = {
    "autoPlayTimes": 0,
    "dailyLessonTimes": 0,
    "musicCourseFreeChallengeTimes": 0,
}


def most_recent_reset(now_micros: int) -> int:
    """Epoch-micros of the most recent 05:00 JST boundary at or before ``now``."""
    now = datetime.datetime.fromtimestamp(now_micros / _MICRO, _JST)
    boundary = now.replace(hour=5, minute=0, second=0, microsecond=0)
    if now < boundary:
        boundary -= datetime.timedelta(days=1)
    return int(boundary.timestamp() * _MICRO)


async def refresh_daily_limits(app, user_id) -> None:
    """Restore the caller's daily allowances to their max if the 05:00 JST reset has passed
    since the last refresh. No-op without a user / DailyLimit row, or if already refreshed.
    """
    if user_id is None:
        return
    now = int(time.time() * _MICRO)
    async with app.acquire_db() as conn:
        row = await conn.fetchrow(get_daily_limits(user_id))
        if row is None or (row.lastRefreshedAt or 0) >= most_recent_reset(now):
            return
        data = row.model_dump()
        for field, cap in DAILY_MAX.items():
            data[field] = max(data.get(field) or 0, cap)  # top up, never reduce
        data["lastRefreshedAt"] = now
        await conn.execute(update_daily_limit(user_id, data))
