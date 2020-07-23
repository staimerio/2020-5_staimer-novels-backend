"""Model for chapters"""

# SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

# SQLAlchemy_serializer
from sqlalchemy_serializer import SerializerMixin

# Services
from services.sqlalchemy.base import Base

# Time
from datetime import datetime


class Chapter(Base, SerializerMixin):
    """Chapter Model"""
    __tablename__ = "chapters"

    """Attributes"""
    chapter = Column(Integer, primary_key=True)
    number = Column(String(10), default="")
    title = Column(String(300))
    novel = Column(Integer, ForeignKey('novels.novel'))
    content = Column(Text)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted_at = Column(DateTime, nullable=True)

    """Relationships"""

    """Serialize settings"""
    serialize_only = (
        'chapter', 'number', 'content', 'created_at', 'title'
    )
