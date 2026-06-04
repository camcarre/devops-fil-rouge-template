from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class CategoryCreate(BaseModel):
    name: str
    description: str | None = None


class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    created_at: datetime


class TopicCreate(BaseModel):
    title: str


class TopicOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    category_id: int
    user_id: int
    created_at: datetime


class PostCreate(BaseModel):
    content: str


class PostOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str
    topic_id: int
    user_id: int
    created_at: datetime
