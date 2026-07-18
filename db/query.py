from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class SelectQuery(Generic[T]):
    def __init__(self, model: type[T], sql: str, *args):
        self.sql = sql
        self.args = args
        self.model = model

    def __str__(self):
        return f"SelectQuery(sql={self.sql.strip()}, args={self.args}, model={self.model.__name__})"


class ExecutableQuery:
    def __init__(self, sql: str, *args):
        self.sql = sql
        self.args = args

    def __str__(self):
        return f"ExecutableQuery(sql={self.sql.strip()}, args={self.args})"
