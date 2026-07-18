# Database Migrations

Each database change is versioned, for easier development.

When you make a database change that modifies an existing table, make a migration
script for it, and add the version numbers. Not required for new tables (those are
handled by `scripts/database_setup.py`).

The main migration script loads an existing database, reads its version number, and
applies the necessary migration scripts in order.

### Initial setup

In the root directory, run `python -m scripts.database_setup` once to create the
tables and seed the version row.

### Running migrations

In the root directory, run `python -m scripts.database_migration.migrate`.

### Adding a migration

1. Create `migrate_<N>_to_<M>.py` in this folder with a
   `def run(db: PostgresqlDatabase) -> int:` that performs the change and returns
   the new version number.
2. Import it in `migrate.py` and register it in the `migrations` dict, keyed by the
   version it upgrades *from*.
3. Bump `version` in `scripts/database_setup.py` if an existing table changed.
