from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class LeaderSenseDetailConditionMaster(BaseModel):
    category_master_id1: Optional[int] = None
    category_master_id2: Optional[int] = None
    category_master_id3: Optional[int] = None
    category_master_id4: Optional[int] = None
    category_master_id5: Optional[int] = None
