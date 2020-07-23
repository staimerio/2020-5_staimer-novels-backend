"""Model for folder with files"""

# SQLAlchemy
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy import ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

# SQLAlchemy_serializer
from sqlalchemy_serializer import SerializerMixin

# Services
from services.sqlalchemy.base import Base

# Time
from datetime import datetime


class NovelPost(Base, SerializerMixin):
    __tablename__ = "novels_posts"

    post = Column(Integer, primary_key=True)
    novel = Column(Integer, ForeignKey('novels.novel'), primary_key=True)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted_at = Column(DateTime, nullable=True)

    """Relationships"""
    novels = relationship("Novel", foreign_keys=[novel])

    """Serialize settings"""
    serialize_only = (
        'novel', 'post'
    )
