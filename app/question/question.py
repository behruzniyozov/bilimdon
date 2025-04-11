from fastapi import APIRouter, Depends, HTTPException, Response
from question.schema import *
from app.models import *
from app.database import get_db

from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.database import get_db, get_current_user  

router = APIRouter()

router.get("/read-questions", response_model=ReadQuestion)
async def get_questions(
    db: get_db,
    user: ReadQuestion
):
    questions = db.query(Question).filter(Question.id==user.id).all()
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found")
    return questions



router = APIRouter()

@router.post("/create-questions", response_model=CreateQuestion)
async def create_question(
    question_data: CreateQuestion,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="You are not allowed to create a question")

    db_question = Question(
        owner_id=current_user.id,
        title=question_data.title,
        description=question_data.description,
        topic=question_data.topic,
        options=question_data.options,
        created_at=datetime.now(timezone.utc),
    )

    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@router.patch("/update-questions/{question_id}", response_model=UpdateQuestion)
async def update_question(
    question_data: UpdateQuestion,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_question = db.query(Question).filter(Question.id == question_data.id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")

    if db_question.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="You are not allowed to update this question")

    db_question.title = question_data.title
    db_question.description = question_data.description
    db_question.topic = question_data.topic
    db_question.options = question_data.options
    db_question.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(db_question)
    return db_question

@router.delete("/delete-questions/{question_id}")
async def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")

    if db_question.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this question")

    db.delete(db_question)
    db.commit()
    return db_question