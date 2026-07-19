from db.query import SelectQuery
from models.database import AccountModel, HashUserIdModel, SequenceValueModel


def next_user_id() -> SelectQuery[SequenceValueModel]:
    return SelectQuery(SequenceValueModel, "SELECT nextval('user_id_seq') AS value")


def get_user_id_by_hash(hash_user_id: str) -> SelectQuery[HashUserIdModel]:
    return SelectQuery(
        HashUserIdModel,
        'SELECT * FROM "hash_user_id" WHERE "hashUserId" = $1',
        hash_user_id,
    )


def get_account_by_id(user_id: int) -> SelectQuery[AccountModel]:
    return SelectQuery(
        AccountModel, 'SELECT * FROM "accounts" WHERE "userId" = $1', user_id
    )


def get_account_by_credential(credential: str) -> SelectQuery[AccountModel]:
    return SelectQuery(
        AccountModel, 'SELECT * FROM "accounts" WHERE "credential" = $1', credential
    )


def get_account_by_token(api_token: str) -> SelectQuery[AccountModel]:
    return SelectQuery(
        AccountModel, 'SELECT * FROM "accounts" WHERE "apiToken" = $1', api_token
    )
