from fastapi import APIRouter, Depends, HTTPException
from app.models import *
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.database import get_db, get_current_user
from topic.schemas import *

router = APIRouter()

@router.get("/read-topics", response_model=ReadTopic)
async def get_topics(
    user: ReadTopic,
    db: Session = Depends(get_db)):
    
    topics = db.query(Topic).filter(Topic.id==user.id).all()
    if not topics:
        raise HTTPException(status_code=404, detail="No topics found")
    return topics


@router.post("/create-topics", response_model=CreateTopic)
async def create_topic(
    topic_data: CreateTopic,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="You are not allowed to create a topic")

    db_topic = Topic(
        name=topic_data.name,
        created_at=datetime.now(timezone.utc),
    )

    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

@router.patch("/update-topics/{topic_id}", response_model=UpdateTopic)
async def update_topic(
    topic_data: UpdateTopic,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_topic = db.query(Topic).filter(Topic.id == topic_data.id).first()
    if not db_topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    if db_topic.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="You are not allowed to update this topic")

    db_topic.name = topic_data.name
    db_topic.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_topic)
    return db_topic

@router.delete("/delete-topics/{topic_id}")
async def delete_topic(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not db_topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    if db_topic.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this topic")

    db.delete(db_topic)
    db.commit()
    return "Topic deleted successfully"