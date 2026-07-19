"""Seed a brand-new account's default data (from a captured Data_GetUserData).

``default_account.json`` holds the initial entities of a fresh account (User,
UserProfile, Currency, starting Characters/Parties/Missions/Inbox, ...) as
camelCase DB rows with no account identity baked in. On registration each row is
inserted for the new userId: the account-singleton entities take the new userId as
their ``id``, and the chosen player name is applied to the profile.
"""

import json
import random
import re
import string
import time
from pathlib import Path

import db.user as db_user
from helpers.user_hash import hash_id

_SEED = json.loads(
    (Path(__file__).resolve().parent / "default_account.json").read_text(
        encoding="utf-8"
    )
)
# entities that are 1:1 with the account -- their id is the userId
_ACCOUNT_ENTITIES = {
    "User",
    "UserProfile",
    "HomeDisplayPreference",
    "UserPreference",
    "UserBonus",
    "Currency",
    "Restriction",
    "Notification",
}
_INBOX_TTL_MICROS = 30 * 86400 * 1_000_000  # packages are claimable for 30 days


def _table(type_name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", type_name).lower()


def _invitation_code() -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))


async def create_default_user_data(conn, user_id: int, name: str) -> None:
    now = int(time.time() * 1_000_000)  # epoch microseconds
    for type_name, rows in _SEED.items():
        upsert = getattr(db_user, f"upsert_{_table(type_name)}", None)
        if upsert is None:  # entity has no table yet (e.g. PartySlot)
            continue
        sql = None
        args_seq = []
        for row in rows:
            row = dict(row)
            if type_name in _ACCOUNT_ENTITIES:
                row["id"] = user_id
            if type_name == "User":
                row["hashUserId"] = hash_id(user_id)
                row["gameStartAt"] = now  # account created now
                row["maxStaminaRestoredAt"] = now  # starts at full stamina
            if type_name == "UserProfile":
                row["name"] = name
            if type_name == "FriendInvitation":
                row["invitationCode"] = _invitation_code()
            if type_name == "MissionPass":
                row["id"] = random.randint(1_000_000, 999_999_999)
            if type_name == "DailyLimit":
                row["lastRefreshedAt"] = now
            if (
                type_name == "Inbox"
            ):  # anchor the claim window to signup, not the capture
                row["sentAt"] = now
                row["receiveLimitAt"] = now + _INBOX_TTL_MICROS
            query = upsert(user_id, row)
            sql = query.sql  # identical for every row of a table
            args_seq.append(query.args)
        if sql is not None:  # one batched round-trip per table instead of one per row
            await conn.execute_batch(sql, args_seq)
