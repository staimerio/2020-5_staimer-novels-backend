"""Model for chapters"""

# SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean

# SQLAlchemy_serializer
from sqlalchemy_serializer import SerializerMixin

# Services
from services.sqlalchemy.base import Base

# Time
from datetime import datetime


class Language(Base, SerializerMixin):
    """Language Model"""
    __tablename__ = "languages"

    """Attributes"""
    language = Column(Integer, primary_key=True)
    title = Column(String(20))
    hreflang = Column(String(2), unique=True)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted_at = Column(DateTime, nullable=True)

    """Relationships"""

    """Serialize settings"""
    serialize_only = (
        'language', 'title'
    )
