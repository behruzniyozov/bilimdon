from pydantic import BaseModel


class ReadQuestionResponse(BaseModel):
    id: int
    owner: str
    title: str
    description: str
    topic: str
    options: list[str]
    created_at: str
    updated_at: str

class ReadQuestion(BaseModel):
    id: int
    owner: str
    title: str
    description: str
    topic: str
    options: list[str]
    created_at: str
    updated_at: str
   
class CreateQuestion(BaseModel):
    id: int
    title: str
    description: str
    topic: str
    options: list[str]
    owner: str

class UpdateQuestion(BaseModel):
    title: str
    description: str
    topic: str
    options: list[str]
    owner: str




