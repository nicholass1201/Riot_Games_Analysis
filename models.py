from pydantic import BaseModel

class UserRequest(BaseModel):
    game_name: str
    tag_line: str

class MatchChoiceRequest(BaseModel):
    game_name: str
    tag_line: str
    match_index: int
