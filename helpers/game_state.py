"""Per-account transactional state for multi-step gameplay writes.

A ``State`` caches the caller's rows for the duration of one advisory-locked transaction,
tracks what it changed, and can emit the ``present`` diff the client expects. Costs/limits
come from master data. Mutations are atomic and serialized per account.
"""

import struct
from contextlib import asynccontextmanager

from db import user as queries
from helpers.cache import cache
from helpers.things import grant_things_consolidated, present_type
from helpers.user_data import _table, _to_array, current_user_id
from models.unions import IDATA_OBJECT_KEY


class Rejected(Exception):
    """Raised to abort and roll back a gameplay action (caller returns a failure result)."""


class NotEnough(Rejected):
    """Raised when the account cannot afford a cost; callers map it to NotEnoughThing."""


def master(table: str, ident, field: str = "id_"):
    return next((x for x in getattr(cache, table) if getattr(x, field) == ident), None)


def f32(value: float) -> float:
    """Round-trip through float32, matching the client's single-precision bonus fields."""
    return struct.unpack("<f", struct.pack("<f", value))[0]


class State:
    # entities whose per-user primary key is not "id"
    _KEY_FIELD = {
        "Episode": "episodeMasterId",
        "ConcertStage": "concertStageMasterId",
        "HomeBGM": "homeBGMMasterId",
        "CharacterLesson": "characterBaseMasterId",
    }

    def __init__(self, conn, uid: int):
        self.conn, self.uid = conn, uid
        self.tables: dict = {}
        self.dirty: dict = {}

    async def rows(self, name: str) -> list:
        if name not in self.tables:
            # table names come only from the implementation, never the request
            self.tables[name] = [
                dict(x)
                for x in await self.conn.conn.fetch(
                    f'SELECT * FROM "{_table(name)}" WHERE "userId"=$1', self.uid
                )
            ]
        return self.tables[name]

    async def one(self, name: str, **where):
        return next(
            (
                r
                for r in await self.rows(name)
                if all(r.get(k) == v for k, v in where.items())
            ),
            None,
        )

    @classmethod
    def key_field(cls, name: str) -> str:
        return cls._KEY_FIELD.get(name, "id")

    async def update(self, entity: str, row, **values) -> None:
        if row is None:
            raise Rejected("Missing account record")
        if not values:
            return
        pk = self.key_field(entity)
        columns = ", ".join(f'"{k}"=${i + 3}' for i, k in enumerate(values))
        await self.conn.conn.execute(
            f'UPDATE "{_table(entity)}" SET {columns} WHERE "userId"=$1 AND "{pk}"=$2',
            self.uid,
            row[pk],
            *values.values(),
        )
        row.update(values)
        self.dirty[(entity, row[pk])] = row.copy()

    async def insert(self, entity: str, **values) -> dict:
        rows = await self.rows(entity)
        pk = self.key_field(entity)
        if pk == "id":
            values.setdefault("id", max([r["id"] for r in rows] + [0]) + 1)
        query = getattr(queries, "upsert_" + _table(entity))(self.uid, values)
        await self.conn.execute(query)
        row = dict(
            await self.conn.conn.fetchrow(
                f'SELECT * FROM "{_table(entity)}" WHERE "userId"=$1 AND "{pk}"=$2',
                self.uid,
                values[pk],
            )
        )
        rows.append(row)
        self.dirty[(entity, row[pk])] = row.copy()
        return row

    async def pay(self, costs: dict, coin: int = 0) -> None:
        if coin < 0 or any(n < 0 for n in costs.values()):
            raise Rejected("Invalid cost")
        items = {r["itemMasterId"]: r for r in await self.rows("Item")}
        currency = await self.one("Currency")
        if any(items.get(i, {}).get("stock", 0) < n for i, n in costs.items()) or (
            coin and (not currency or currency["coin"] < coin)
        ):
            raise NotEnough("Insufficient resources")
        for i, n in costs.items():
            if n:
                await self.update("Item", items[i], stock=items[i]["stock"] - n)
        if coin:
            await self.update("Currency", currency, coin=currency["coin"] - coin)

    async def grant(self, things) -> list:
        if not things:
            return []
        names = {present_type(t) for t, _, _ in things} - {None}
        snapshots = {
            name: {r["id"]: r.copy() for r in await self.rows(name)} for name in names
        }
        result = await grant_things_consolidated(self.conn, self.uid, things)
        # grant helpers can create several resource types; reload just the affected rows
        for name in names:
            before = snapshots[name]
            self.tables.pop(name, None)
            for row in await self.rows(name):
                if before.get(row["id"]) != row:
                    self.dirty[(name, row[self.key_field(name)])] = row.copy()
        return result

    def present(self) -> list:
        return [
            [IDATA_OBJECT_KEY[n], _to_array(n, r)] for (n, _), r in self.dirty.items()
        ]


@asynccontextmanager
async def transaction(request):
    uid = current_user_id(request)
    if uid is None:
        raise Rejected("Authentication required")
    async with request.app.acquire_db() as conn, conn.transaction():
        await conn.conn.execute("SELECT pg_advisory_xact_lock($1)", uid)
        yield State(conn, uid)


async def character_progress(s: State, base: int, mission_id: int, delta: int) -> None:
    if delta <= 0:
        return
    m = master("character_mission_master", mission_id)
    if not m:
        return
    stages = sorted(m.stages or [], key=lambda x: x.stage_order)
    if not stages:
        return
    row = await s.one(
        "CharacterMission",
        characterBaseMasterId=base,
        characterMissionMasterId=mission_id,
    )
    count = (row["currentCount"] if row else 0) + delta
    cleared = max([x.stage_order for x in stages if x.goal_count <= count] + [0])
    if row:
        await s.update(
            "CharacterMission",
            row,
            currentCount=count,
            clearedStageOrder=max(cleared, row["clearedStageOrder"]),
        )
    else:
        await s.insert(
            "CharacterMission",
            characterBaseMasterId=base,
            characterMissionMasterId=mission_id,
            currentStageMasterId=stages[0].id_,
            currentCount=count,
            clearedStageOrder=cleared,
            rewardReceivedStageOrder=0,
            completedLevel=0,
        )


async def mission_progress(
    s: State, ident: int, delta: int = 1, *, create: bool = False, absolute=None
) -> None:
    m = master("mission_master", ident)
    if not m or not m.stages:
        return
    row = await s.one("Mission", missionMasterId=ident)
    if not row and not create:
        return
    stage = next(
        (x for x in m.stages if row and x.id_ == row["currentMissionStageMasterId"]),
        m.stages[0],
    )
    old = row["missionCurrentCount"] if row else 0
    count = max(old, absolute) if absolute is not None else old + delta
    cleared = count >= stage.stage_goal_value
    newly = cleared and (not row or not row["isCleared"])
    if row:
        await s.update(
            "Mission",
            row,
            missionCurrentCount=count,
            isCleared=row["isCleared"] or cleared,
        )
    else:
        await s.insert(
            "Mission",
            missionMasterId=ident,
            currentMissionStageMasterId=stage.id_,
            missionCurrentCount=count,
            isCleared=cleared,
            isRewardReceived=False,
        )
    if newly and 1 <= ident < 42:
        await mission_progress(s, 42)
        if ident % 6:
            await mission_progress(s, ((ident - 1) // 6 + 1) * 6)


async def costume_owned(s: State, base: int, ident: int) -> None:
    """Validate that character base ``base`` may wear costume ``ident`` (default costumes and
    group-wearable costumes are allowed; anything else must be owned). Raises ``Rejected``."""
    b = master("character_base_master", base)
    c = master("costume_master", ident)
    if not b or not c or not await s.one("CharacterBase", characterBaseMasterId=base):
        raise Rejected()
    group = master("costume_group_master", c.costume_group_master_id)
    wearable = (
        master(
            "costume_wearable_character_group_master",
            group.costume_wearable_character_group_master_id,
        )
        if group
        else None
    )
    if wearable and base not in (wearable.character_base_master_ids or []):
        raise Rejected()
    if (
        not c.is_default
        and b.default_costume_master_id != ident
        and not await s.one("Costume", costumeMasterId=ident)
    ):
        raise Rejected()


async def star_points(s: State, base: int, points: int):
    """Add ``points`` star points to a character base, ranking it up and granting the
    star-rank rewards crossed. Returns a ``StarPointResult``."""
    from models import StarPointResult

    row = await s.one("CharacterBase", characterBaseMasterId=base)
    if not row:
        raise Rejected()
    before = row["starRank"]
    rank = before
    old = row["totalStarPoint"]
    balance = old + points
    while True:
        m = master("character_star_rank_master", rank, "rank")
        if (
            not m
            or m.next_rank_point <= 0
            or balance < m.next_rank_point
            or not master("character_star_rank_master", rank + 1, "rank")
        ):
            break
        balance -= m.next_rank_point
        rank += 1
    await s.update("CharacterBase", row, starRank=rank, totalStarPoint=balance)
    things = []
    for r in cache.star_rank_reward_master:
        if r.character_base_master_id == base and before < r.rank <= rank:
            group = master(
                "character_star_rank_reward_group_master",
                r.character_star_rank_reward_group_master_id,
            )
            things.extend(
                (int(x.thing_type), x.thing_id, x.thing_quantity)
                for x in group.rewards or []
            )
    received = await s.grant(things)
    return StarPointResult(
        rank_before=before,
        rank_after=rank,
        star_point_before=old,
        star_point_after=balance,
        star_point_acquired=points,
        received_reward=received,
    )


async def level_missions(s: State, cm, delta: int, level: int) -> None:
    if delta <= 0:
        return
    base = master("character_base_master", cm.character_base_master_id)
    await character_progress(s, cm.character_base_master_id, 3, delta)
    await mission_progress(s, 1200, delta)
    if base:
        await mission_progress(s, base.company_master_id * 100 + 20, delta)
    for mid in (300030, 300100):
        await mission_progress(s, mid, delta)
    if level >= 10:
        await mission_progress(s, 8, absolute=1, create=True)
