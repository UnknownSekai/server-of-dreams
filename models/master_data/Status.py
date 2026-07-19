from __future__ import annotations

from pydantic import BaseModel


class Status(BaseModel):
    concentration: int = 0
    expression: int = 0
    vocal: int = 0
