from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

import asyncpg
from fastapi import FastAPI

from db import DBConnWrapper
from db.utils import create_dsn
from helpers.config import Database


class YumeApp(FastAPI):
    def __init__(self, config: Optional[Database] = None, **kwargs):
        super().__init__(**kwargs)
        self.config: Optional[Database] = config
        self._db: asyncpg.Pool
        self.is_setup: bool = False

    async def yume_setup(self) -> None:
        if self.is_setup:
            return
        if self.config is None:
            raise AttributeError("No 'database' section in config.yml")
        dsn = create_dsn(
            self.config.host,
            self.config.port,
            self.config.database,
            self.config.username,
            self.config.password,
        )
        self._db = await asyncpg.create_pool(
            dsn,
            min_size=self.config.settings.min_size,
            max_size=self.config.settings.max_size,
        )
        self.is_setup = True

    async def close(self) -> None:
        if self.is_setup:
            await self._db.close()
            self.is_setup = False

    @asynccontextmanager
    async def acquire_db(self) -> AsyncGenerator[DBConnWrapper, None]:
        if not self.is_setup:
            raise AttributeError("setup has not been called.")
        async with self._db.acquire() as conn:
            yield DBConnWrapper(conn)
