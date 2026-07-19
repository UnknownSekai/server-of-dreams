"""Wipe the entire database: drop every table and sequence in the 'public' schema.

Reads the DB connection from the same config the app uses (config.yml by default,
override with --config), exactly like scripts/database_setup.py.

    python scripts/database_reset.py                 # prompts for confirmation
    python scripts/database_reset.py --yes            # no prompt (for automation)
    python scripts/database_reset.py --config other.yml

This is destructive and cannot be undone. Afterwards run scripts/database_setup.py
to recreate the schema (it restores user_id_seq and all tables).
"""

import argparse
import sys

import yaml
from peewee import PostgresqlDatabase

from helpers.config import Database


def _fetch_names(db: PostgresqlDatabase, sql: str) -> list[str]:
    return [row[0] for row in db.execute_sql(sql).fetchall()]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Wipe the entire database (drops all tables and sequences)."
    )
    parser.add_argument("--config", default="config.yml", help="Path to config file")
    parser.add_argument(
        "--yes", action="store_true", help="Skip the confirmation prompt"
    )
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        cfg = Database(**yaml.safe_load(f)["database"])

    db = PostgresqlDatabase(
        cfg.database,
        user=cfg.username,
        password=cfg.password,
        host=cfg.host,
        port=cfg.port,
    )
    # Skip objects owned by an extension (e.g. PostGIS's spatial_ref_sys): the app role
    # can't drop them and doesn't create them, and trying would abort the whole wipe.
    _not_extension = "NOT EXISTS (SELECT 1 FROM pg_depend d WHERE d.objid = c.oid AND d.deptype = 'e')"

    db.connect()
    try:
        tables = _fetch_names(
            db,
            "SELECT c.relname FROM pg_class c "
            "JOIN pg_namespace n ON n.oid = c.relnamespace "
            f"WHERE n.nspname = 'public' AND c.relkind = 'r' AND {_not_extension} "
            "ORDER BY c.relname",
        )
        sequences = _fetch_names(
            db,
            "SELECT c.relname FROM pg_class c "
            "JOIN pg_namespace n ON n.oid = c.relnamespace "
            f"WHERE n.nspname = 'public' AND c.relkind = 'S' AND {_not_extension} "
            "ORDER BY c.relname",
        )

        if not tables and not sequences:
            print("Database already empty (no tables or sequences in 'public').")
            return

        print(
            f"About to DROP {len(tables)} table(s) and {len(sequences)} sequence(s) "
            f"from '{cfg.database}' @ {cfg.host}:{cfg.port}."
        )
        if not args.yes:
            answer = input(
                "This CANNOT be undone. Type the database name to confirm: "
            ).strip()
            if answer != cfg.database:
                print("Confirmation did not match. Aborted.")
                sys.exit(1)

        # DDL is transactional in Postgres -> all-or-nothing. CASCADE clears FKs, and
        # dropping tables also drops their owned (AutoField) sequences, so the leftover
        # sequence drops use IF EXISTS.
        with db.atomic():
            for name in tables:
                db.execute_sql(f'DROP TABLE IF EXISTS "{name}" CASCADE')
            for name in sequences:
                db.execute_sql(f'DROP SEQUENCE IF EXISTS "{name}" CASCADE')

        print(
            f"Wiped {len(tables)} table(s) and {len(sequences)} sequence(s). "
            "Database is now empty."
        )
        print("Run scripts/database_setup.py to recreate the schema.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
