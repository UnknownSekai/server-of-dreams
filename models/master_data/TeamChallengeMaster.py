from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from models.enums import TeamChallengeDifficultyTypes, TeamChallengeGoalTypes


class TeamChallengeMaster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id_: int = Field(default=0, alias="id")
    music_master_id: int = 0
    difficulty: TeamChallengeDifficultyTypes = TeamChallengeDifficultyTypes.Easy
    goal_type: TeamChallengeGoalTypes = TeamChallengeGoalTypes.TotalScore
    goal_min_value: int = 0
    goal_max_value: int = 0
    start_date: str = ""
    end_date: str = ""
