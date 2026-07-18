import argparse
from typing import Callable, Dict

import yaml
from peewee import IntegerField, Model, PostgresqlDatabase

from helpers.config import Database

_parser = argparse.ArgumentParser()
_parser.add_argument("--config", default="config.yml", help="Path to config file")
_args = _parser.parse_args()

with open(_args.config, "r", encoding="utf-8") as f:
    CONFIG = Database(**yaml.safe_load(f)["database"])

db = PostgresqlDatabase(
    CONFIG.database,
    user=CONFIG.username,
    password=CONFIG.password,
    host=CONFIG.host,
    port=CONFIG.port,
)

migrations: Dict[int, Callable[[PostgresqlDatabase], int]] = {}


class BaseModel(Model):
    class Meta:
        database = db


class DatabaseInfo(BaseModel):
    version = IntegerField(unique=True, primary_key=True, null=False)


def main():
    db.connect()
    current_version = DatabaseInfo.get().version
    while current_version in migrations:
        print(f"Running migration for version {current_version}...")
        new_version = migrations[current_version](db)
        current_version = new_version
        DatabaseInfo.update(version=current_version).execute()
        print(f"Migration to version {current_version} complete.")
    db.close()
    print("All migrations complete.")


main()
