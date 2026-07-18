from db.query import SelectQuery
from models.database import AccountModel


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
