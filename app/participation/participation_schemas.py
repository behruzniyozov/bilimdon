from pydantic import BaseModel


class ReadParticipation(BaseModel):
    id: int
    user_id: int
    game_id: int
    start_time: str
    end_time: str
    gained_score: int
    registered_at: str

class ReadParticipant(BaseModel):
    id: int
    gained_score: int
    registered_at: str


class CreateParticipation(BaseModel):
    user_id: int
    game_id: int
    start_time: str
    end_time: str
    gained_score: int

class UpdateParticipation(BaseModel):
    user_id: int
    game_id: int
    start_time: str
    end_time: str
    gained_score: int
