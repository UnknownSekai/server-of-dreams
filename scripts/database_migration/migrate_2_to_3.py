"""v2 -> v3: store the takeover password / linkage / confirmation state.

``connect_with_password`` previously carried only ``id``. The account-link flow needs
four more columns:

* ``passwordHash``         -- argon2 hash of the takeover password
* ``linkageCode``          -- the 10 digit code shown to the player, paired with the password
* ``confirmationCode``     -- the 6 digit code from ``/api/Account/GetConfirmationCode``
* ``confirmationExpiresAt``-- unix seconds the confirmation code stops being valid

``userId`` also becomes unique: the flow is one password per account, which lets
``upsert_connect_with_password`` use ``ON CONFLICT ("userId")``.
"""

from peewee import PostgresqlDatabase


def run(db: PostgresqlDatabase) -> int:
    db.execute_sql(
        'ALTER TABLE "connect_with_password" '
        'ADD COLUMN IF NOT EXISTS "passwordHash" text'
    )
    db.execute_sql(
        'ALTER TABLE "connect_with_password" '
        'ADD COLUMN IF NOT EXISTS "linkageCode" text'
    )
    db.execute_sql(
        'ALTER TABLE "connect_with_password" '
        'ADD COLUMN IF NOT EXISTS "confirmationCode" text'
    )
    db.execute_sql(
        'ALTER TABLE "connect_with_password" '
        'ADD COLUMN IF NOT EXISTS "confirmationExpiresAt" bigint NOT NULL DEFAULT 0'
    )
    # one password pairing per account, so the upsert can key on userId
    db.execute_sql(
        'DELETE FROM "connect_with_password" a USING "connect_with_password" b '
        'WHERE a."userId" = b."userId" AND a."rowId" < b."rowId"'
    )
    db.execute_sql(
        'CREATE UNIQUE INDEX IF NOT EXISTS "connectwithpassword_userId_unique" '
        'ON "connect_with_password" ("userId")'
    )
    db.execute_sql(
        'CREATE UNIQUE INDEX IF NOT EXISTS "connectwithpassword_linkageCode_unique" '
        'ON "connect_with_password" ("linkageCode") WHERE "linkageCode" IS NOT NULL'
    )
    return 3
