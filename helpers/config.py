from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel

config: dict = (
    yaml.safe_load(
        (Path(__file__).resolve().parent.parent / "config.yml").read_text(
            encoding="utf-8"
        )
    )
    or {}
)


class DatabaseSettings(BaseModel):
    min_size: int = 3
    max_size: int = 20


class Database(BaseModel):
    host: str
    port: int
    database: str
    username: str
    password: str
    settings: DatabaseSettings = DatabaseSettings()


database: Optional[Database] = (
    Database(**config["database"]) if config.get("database") else None
)
