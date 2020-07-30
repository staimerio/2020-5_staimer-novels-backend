"""Model for volumes"""

# SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import ForeignKey

# SQLAlchemy_serializer
from sqlalchemy_serializer import SerializerMixin

# Services
from services.sqlalchemy.base import Base

# Time
from datetime import datetime


class Request(Base, SerializerMixin):
    """Request Model"""
    __tablename__ = "requests"

    """Attributes"""
    request = Column(Integer, primary_key=True)
    title = Column(String(300))
    email = Column(String(200))
    reference = Column(String(200))
    language = Column(Integer, ForeignKey('languages.language'))
    is_completed = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted_at = Column(DateTime, nullable=True)

    """Relationships"""

    """Serialize settings"""
    serialize_only = (
        'request', 'title', 'language',
        'reference', 'created_at', 'is_completed'
    )
