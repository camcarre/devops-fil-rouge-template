from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.models.category import Category
from src.models.topic import Topic
from src.models.user import User
from src.schemas import TopicCreate, TopicOut
from src.security import get_current_user

router = APIRouter(prefix="/categories", tags=["topics"])


@router.get("/{category_id}/topics", response_model=List[TopicOut])
def list_topics(category_id: int, db: Session = Depends(get_db)):
    if not db.query(Category).filter(Category.id == category_id).first():
        raise HTTPException(status_code=404, detail="Category not found")
    return db.query(Topic).filter(Topic.category_id == category_id).all()


@router.post("/{category_id}/topics", response_model=TopicOut, status_code=201)
def create_topic(
    category_id: int,
    body: TopicCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not db.query(Category).filter(Category.id == category_id).first():
        raise HTTPException(status_code=404, detail="Category not found")
    topic = Topic(title=body.title, category_id=category_id, user_id=current_user.id)
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic
