from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.models.post import Post
from src.models.topic import Topic
from src.models.user import User
from src.schemas import PostCreate, PostOut
from src.security import get_current_user

router = APIRouter(prefix="/topics", tags=["posts"])


@router.get("/{topic_id}/posts", response_model=List[PostOut])
def list_posts(topic_id: int, db: Session = Depends(get_db)):
    if not db.query(Topic).filter(Topic.id == topic_id).first():
        raise HTTPException(status_code=404, detail="Topic not found")
    return db.query(Post).filter(Post.topic_id == topic_id).all()


@router.post("/{topic_id}/posts", response_model=PostOut, status_code=201)
def create_post(
    topic_id: int,
    body: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not db.query(Topic).filter(Topic.id == topic_id).first():
        raise HTTPException(status_code=404, detail="Topic not found")
    post = Post(content=body.content, topic_id=topic_id, user_id=current_user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post
