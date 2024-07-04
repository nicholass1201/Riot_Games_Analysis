from pydantic import BaseModel
from typing import Dict, Any

class UserRequest(BaseModel):
    game_name: str
    tag_line: str

class MatchChoiceRequest(BaseModel):
    game_name: str
    tag_line: str
    match_index: int

class MatchAnalysisBase(BaseModel):
    match_id: str
    good_player_name: str
    good_player_stats: Dict[str, Any]
    bad_player_name: str
    bad_player_stats: Dict[str, Any]
    analysis: str

class MatchAnalysisCreate(MatchAnalysisBase):
    pass

class MatchAnalysis(MatchAnalysisBase):
    id: int

    class Config:
        orm_mode = True
