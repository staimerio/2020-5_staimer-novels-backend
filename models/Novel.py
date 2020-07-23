"""Model for volumes"""

# SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean

# SQLAlchemy_serializer
from sqlalchemy_serializer import SerializerMixin

# Services
from services.sqlalchemy.base import Base

# Time
from datetime import datetime


class Novel(Base, SerializerMixin):
    """Novel Model"""
    __tablename__ = "novels"

    """Attributes"""
    novel = Column(Integer, primary_key=True)
    title = Column(String(300))
    slug = Column(String(200), unique=True)
    site = Column(String(100))
    url = Column(String(200))
    year = Column(Integer)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted_at = Column(DateTime, nullable=True)

    """Relationships"""

    """Serialize settings"""
    serialize_only = (
        'novel', 'title', 'slug', 'site',
        'url', 'year', 'created_at',
    )
