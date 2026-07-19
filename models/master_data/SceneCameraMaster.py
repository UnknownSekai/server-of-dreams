from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class SceneCameraMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    start_position_x: int = 0
    start_position_y: int = 0
    start_zoom_ratio: int = 0
    end_position_x: int = 0
    end_position_y: int = 0
    end_zoom_ratio: int = 0
    camera_move_turnaround_time_seconds: int = 0
