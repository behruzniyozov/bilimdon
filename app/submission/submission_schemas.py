from pydantic import BaseModel


class ReadSubmission(BaseModel):
    id: int
    user_id: int
    question_id: int 
    option_id: int
    is_correct: bool 
    created_at: str 
    

class CreateSubmission(BaseModel):
    user_id: int
    question_id: int 
    option_id: int
    is_correct: bool 
    created_at: str

class UpdateSubmission(BaseModel):
    user_id: int
    question_id: int 
    option_id: int
    is_correct: bool 
    
