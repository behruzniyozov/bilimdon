from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from participation_schemas import *
from app.database import get_db, get_current_user
from app.models import *

router = APIRouter(prefix="/participation", tags=["participation"])

@router.get("/", response_model=List[ReadParticipation])
def get_participations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    participations = db.query(Participation).all()
    return participations

@router.get("/{participation_id}", response_model=ReadParticipant)
def get_participant(
    participation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    participant = db.query(Participation).filter(Participation.id == participation_id).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    return participant

@router.post("/", response_model=CreateParticipation)
def create_participation(
    participation: CreateParticipation,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_participation = Participation(**participation.model_dump())
    db.add(new_participation)
    db.commit()
    db.refresh(new_participation)
    return new_participation

@router.put("/{participation_id}", response_model=UpdateParticipation)
def update_participation(
    participation_id: int,
    participation: UpdateParticipation,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing_participation = db.query(Participation).filter(Participation.id == participation_id).first()
    if not existing_participation:
        raise HTTPException(status_code=404, detail="Participation not found")
    
    for key, value in participation.model_dump().items():
        setattr(existing_participation, key, value)
    
    db.commit()
    db.refresh(existing_participation)
    return existing_participation

@router.delete("/{participation_id}", response_model=ReadParticipation)
def delete_participation(
    participation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing_participation = db.query(Participation).filter(Participation.id == participation_id).first()
    if not existing_participation:
        raise HTTPException(status_code=404, detail="Participation not found")
    
    db.delete(existing_participation)
    db.commit()
    return existing_participation