from pydantic import BaseModel


class ReadGame(BaseModel):
    id: int
    owner: str
    title: str
    description: str
    topic: str
    score: float
    start_time: str
    end_time: str

class CreateGame(BaseModel):
    id: int
    owner: str
    title: str
    description: str
    topic: str
    score: float
    start_time: str
    end_time: str


class UpdateGame(BaseModel):
    id: int
    topic: str
    score: float
    start_time: str
    end_time: str
