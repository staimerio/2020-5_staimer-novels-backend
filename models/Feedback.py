"""Model for volumes"""

# SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import ForeignKey, Text

# SQLAlchemy_serializer
from sqlalchemy_serializer import SerializerMixin

# Services
from services.sqlalchemy.base import Base

# Time
from datetime import datetime


class Feedback(Base, SerializerMixin):
    """Request Model"""
    __tablename__ = "feedback"

    """Attributes"""
    feedback = Column(Integer, primary_key=True)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.now())
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)
    """Relationships"""

    """Serialize settings"""
    serialize_only = (
        'feedback', 'created_at', 'comment'
    )
