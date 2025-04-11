from pydantic import BaseModel

class ReadTopic(BaseModel):
    id: int
    question: str
    title: str
    description: str
    is_correct: bool
    created_at: str
    updated_at: str

class CreateTopic(BaseModel):
    question: str
    title: str
    description: str
    created_at: str


class UpdateTopic(BaseModel):
    id: int
    question: str
    title: str
    description: str
    updated_at: str
    