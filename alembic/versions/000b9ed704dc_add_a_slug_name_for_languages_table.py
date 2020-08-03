"""Add a slug, name for languages table

Revision ID: 000b9ed704dc
Revises: c5bd3840601d
Create Date: 2020-08-01 16:31:50.856315

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


# revision identifiers, used by Alembic.
revision = '000b9ed704dc'
down_revision = 'c5bd3840601d'
branch_labels = None
depends_on = None

LANGUAGES = [
    {
        u'title': "English", u"hreflang": "en",
        u"slug": "novel-updates", u"name": "english"
    },
    {
        u'title': "Español", u"hreflang": "es",
        u"slug": "novela-ligera", u"name": "español"
    }
]


class Language(Base):
    """Language Model"""
    __tablename__ = "languages"

    """Attributes"""
    language = Column(Integer, primary_key=True)
    title = Column(String(20))
    name = Column(String(20))
    slug = Column(String(30), unique=True)
    hreflang = Column(String(2), unique=True)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted_at = Column(DateTime, nullable=True)


def upgrade():
    _bind = op.get_bind()
    _session = orm.Session(bind=_bind)

    op.add_column("languages", sa.Column('name', sa.String(20)))
    op.add_column("languages", sa.Column('slug', sa.String(30), unique=True))

    for _lang in _session.query(Language):
        """Search language"""
        _old_lang = find_lang(LANGUAGES, _lang.hreflang)
        _lang.slug = _old_lang['slug']
        _lang.name = _old_lang['name']
    _session.commit()


def downgrade():
    op.drop_column('languages', 'name')
    op.drop_column('languages', 'slug')


def find_lang(list, hreflang):
    for _item in list:
        if hreflang == _item['hreflang']:
            return _item
    return None
