from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.db.database import Base


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    category = relationship("Category")
    author = relationship("User")
