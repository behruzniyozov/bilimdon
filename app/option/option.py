from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.database import get_db, get_current_user
from app.models import *
from option.option_schemas import *

router= APIRouter(prefix="/option", tags=["Option"])

@router.get("/read-options", response_model=List[ReadOption])
async def read_options(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    options = db.query(Option).all()
    return options

@router.get("/read-options", response_model=ReadOption)
async def read_option(option_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    option = db.query(Option).filter(Option.id == option_id).first()
    if not option:
        raise HTTPException(status_code=404, detail="Option not found")
    return option

@router.post("/create-option", response_model=CreateOption)
async def create_option(option: CreateOption, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_option = Option(**option.model_dump(), created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc))
    db.add(new_option)
    db.commit()
    db.refresh(new_option)
    return new_option

@router.put("/update-option/{option_id}", response_model=UpdateOption)
async def update_option(option_id: int, option: UpdateOption, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing_option = db.query(Option).filter(Option.id == option_id).first()
    if not existing_option:
        raise HTTPException(status_code=404, detail="Option not found")
    for key, value in option.model_dump().items():
        setattr(existing_option, key, value)
    existing_option.updated_at = datetime.now(timezone.utc)
    is_correct = option.is_correct
    db.commit()
    db.refresh(existing_option)
    return existing_option


@router.delete("/delete-option/{option_id}")
async def delete_option(option_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing_option = db.query(Option).filter(Option.id == option_id).first()
    if not existing_option:
        raise HTTPException(status_code=404, detail="Option not found")
    db.delete(existing_option)
    db.commit()
    return  "Option deleted successfully"