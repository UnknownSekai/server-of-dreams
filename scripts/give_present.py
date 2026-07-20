"""Give a thing to a user's present box (inbox), unclaimed.

    python -m scripts.give_present --user 123 --type Jewel --amount 500 --message "Sorry!"
    python -m scripts.give_present --user 123 --type Item --thing-id 130001 --amount 10 -m "Here"

--type is a ThingTypes name (Coin/Jewel/Item/Character/...) or its integer. --thing-id is required
for everything except Coin/Jewel/Stamina (which have no id). The user claims it in-game like any
other present.
"""

import argparse
import datetime
import random
import time

import yaml
from peewee import PostgresqlDatabase

from helpers.config import Database
from models.enums import ThingTypes

_MICRO = 1_000_000
_NO_ID_TYPES = {ThingTypes.Coin, ThingTypes.Jewel, ThingTypes.Stamina}
# receive-by limit; far enough out that the present effectively never expires
_RECEIVE_LIMIT = int(
    datetime.datetime(2100, 1, 1, tzinfo=datetime.timezone.utc).timestamp() * _MICRO
)


def _thing_type(value: str) -> ThingTypes:
    try:
        return ThingTypes(int(value))
    except ValueError:
        for t in ThingTypes:
            if t.name.lower() == value.lower():
                return t
    raise SystemExit(
        f"unknown thing type {value!r}. valid: {', '.join(t.name for t in ThingTypes)}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Give a thing to a user's present box."
    )
    parser.add_argument("--user", type=int, required=True, help="target userId")
    parser.add_argument("--type", required=True, help="ThingTypes name or integer")
    parser.add_argument("--amount", type=int, required=True, help="quantity to grant")
    parser.add_argument(
        "--thing-id",
        type=int,
        default=0,
        help="the thing's master id (required unless Coin/Jewel/Stamina)",
    )
    parser.add_argument(
        "-m", "--message", default="", help="the present's title/message"
    )
    parser.add_argument("--config", default="config.yml", help="path to config file")
    args = parser.parse_args()

    thing_type = _thing_type(args.type)
    if thing_type not in _NO_ID_TYPES and not args.thing_id:
        raise SystemExit(f"--thing-id is required for {thing_type.name}")
    if args.amount <= 0:
        raise SystemExit("--amount must be positive")

    with open(args.config, "r", encoding="utf-8") as f:
        cfg = Database(**yaml.safe_load(f)["database"])
    db = PostgresqlDatabase(
        cfg.database,
        user=cfg.username,
        password=cfg.password,
        host=cfg.host,
        port=cfg.port,
    )
    db.connect()
    try:
        if not db.execute_sql(
            'SELECT 1 FROM "accounts" WHERE "userId" = %s', (args.user,)
        ).fetchone():
            raise SystemExit(f"no account with userId {args.user}")
        message = args.message or None
        db.execute_sql(
            'INSERT INTO "inbox" ("userId", "id", "thingType", "thingId", "thingQuantity", '
            '"isTimeLimited", "hasReceived", "title", "description", "sentAt", "receivedAt", '
            '"receiveLimitAt", "checked") '
            "VALUES (%s, %s, %s, %s, %s, false, false, %s, %s, %s, NULL, %s, false)",
            (
                args.user,
                random.randint(1_000_000, 9_999_999_999),
                int(thing_type),
                args.thing_id,
                args.amount,
                message,
                message,
                int(time.time() * _MICRO),
                _RECEIVE_LIMIT,
            ),
        )
    finally:
        db.close()

    idpart = f" (id {args.thing_id})" if args.thing_id else ""
    print(
        f"Sent {args.amount}x {thing_type.name}{idpart} to user {args.user}'s present box."
    )


if __name__ == "__main__":
    main()
