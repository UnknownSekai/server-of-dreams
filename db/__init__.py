from typing import Optional

from asyncpg import Connection

from . import account, user
from .query import ExecutableQuery, SelectQuery, T


class DBConnWrapper:
    def __init__(self, conn: Connection):
        self._conn = conn

    @property
    def conn(self) -> Connection:
        return self._conn

    def transaction(self):
        return self._conn.transaction()

    async def execute(self, query: ExecutableQuery):
        try:
            return await self._conn.execute(query.sql, *query.args)
        except Exception as e:
            print(query)
            raise e

    async def execute_batch(self, sql: str, args_seq):
        try:
            return await self._conn.executemany(sql, args_seq)
        except Exception as e:
            print(sql)
            raise e

    async def executeAll(self, queries: list[ExecutableQuery]):
        results = []
        for query in queries:
            try:
                results.append(await self._conn.execute(query.sql, *query.args))
            except Exception as e:
                print(query)
                raise e
        return results

    async def fetch(self, query: SelectQuery[T]) -> list[T]:
        try:
            rows = await self._conn.fetch(query.sql, *query.args)
        except Exception as e:
            print(query)
            raise e
        if not rows:
            return []
        return [query.model.model_validate(dict(r)) for r in rows]

    async def fetchrow(self, query: SelectQuery[T]) -> Optional[T]:
        try:
            row = await self._conn.fetchrow(query.sql, *query.args)
        except Exception as e:
            print(query)
            raise e
        if not row:
            return None
        return query.model.model_validate(dict(row))
