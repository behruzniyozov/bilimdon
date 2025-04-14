from pydantic import BaseModel, Field


class ReadOption(BaseModel):
    id: int
    title: str
    is_correct: bool
    created_at: str 
    updated_at: str
    question_id: int
    submission_id: int 

class CreateOption(BaseModel):
    title: str 
    is_correct: bool
    question_id: int 
    submission_id: int

class UpdateOption(BaseModel):
    title: str 
    is_correct: bool 
    question_id: int 
    submission_id: int 