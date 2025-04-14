from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, get_current_user
from app.models import *
from submission.submission_schemas import *


router = APIRouter(prefix="/submission", tags=["submission"])

@router.get("/", response_model=ReadSubmission)
def get_submissions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    submissions = db.query(Submission).all()
    return submissions

@router.get("/{submission_id}", response_model=ReadSubmission)
def get_submission(submission_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return submission

@router.post("/", response_model=CreateSubmission)
def create_submission(submission: CreateSubmission, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_submission = Submission(**submission.model_dump())
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    return new_submission

@router.put("/{submission_id}", response_model=UpdateSubmission)
def update_submission(submission_id: int, submission: UpdateSubmission, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing_submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not existing_submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    for key, value in submission.model_dump().items():
        setattr(existing_submission, key, value)
    
    db.commit()
    db.refresh(existing_submission)
    return existing_submission

@router.delete("/{submission_id}")
def delete_submission(submission_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    db.delete(submission)
    db.commit()
    print("Submission deleted successfully")
    return submission