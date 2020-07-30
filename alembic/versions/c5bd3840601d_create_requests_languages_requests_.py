"""create requests languages requests_novels tables

Revision ID: c5bd3840601d
Revises: 
Create Date: 2020-07-28 23:39:26.007242

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey, orm, Table
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# revision identifiers, used by Alembic.
revision = 'c5bd3840601d'
down_revision = None
branch_labels = None
depends_on = None

LANGUAGES = [
    {u'title': "English", u"hreflang": "en"},
    {u'title': "Español", u"hreflang": "es"}
]
# Declare all models


class Novel(Base):
    """Novel Model"""
    __tablename__ = "novels"

    """Attributes"""
    novel = Column(Integer, primary_key=True)
    title = Column(String(300))
    slug = Column(String(200), unique=True)
    site = Column(String(100))
    url = Column(String(200))
    year = Column(Integer)
    language = Column(Integer, ForeignKey('languages.language'))
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted_at = Column(DateTime, nullable=True)


class Language(Base):
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


def upgrade():
    _bind = op.get_bind()
    _session = orm.Session(bind=_bind)

    # Create tables
    op.create_table("languages",
                    Column("language", Integer, primary_key=True),
                    Column("title", String(20)),
                    Column("hreflang", String(2)),
                    Column("is_active", Boolean, default=True),
                    Column("is_deleted", Boolean, default=False),
                    Column("created_at", DateTime, default=datetime.now()),
                    Column("deleted_at", DateTime, nullable=True)
                    )
    op.create_table("requests",
                    Column("request", Integer, primary_key=True),
                    Column("title", String(300)),
                    Column("email", String(200)),
                    Column("reference", String(200)),
                    Column("language", Integer, ForeignKey(
                        'languages.language')),
                    Column("is_completed", Boolean, default=False),
                    Column("is_active", Boolean, default=True),
                    Column("is_deleted", Boolean, default=False),
                    Column("created_at", DateTime, default=datetime.now()),
                    Column("deleted_at", DateTime, nullable=True)
                    )
    op.create_table("requests_novels_posts",
                    Column("post", Integer, primary_key=True),
                    Column("novel", Integer, ForeignKey(
                        'novels.novel'), primary_key=True),
                    Column("request", Integer, ForeignKey(
                        'requests.request'), primary_key=True),
                    Column("is_active", Boolean, default=True),
                    Column("is_deleted", Boolean, default=False),
                    Column("created_at", DateTime, default=datetime.now()),
                    Column("deleted_at", DateTime, nullable=True)
                    )

    op.add_column("novels", sa.Column('language', sa.Integer,
                                      sa.ForeignKey('languages.language'))
                  )

    # create all default languages
    _languages = [
        Language(
            title=_language["title"],
            hreflang=_language["hreflang"]
        ) for _language in LANGUAGES
    ]
    _session.add_all(_languages)
    _session.flush()
    # set languages for novels
    for _novel in _session.query(Novel):
        _novel.language = _languages[0].language
    _session.commit()


def downgrade():
    op.drop_column('novels', 'language')
    op.drop_table("requests_novels_posts")
    op.drop_table("requests")
    op.drop_table("languages")
