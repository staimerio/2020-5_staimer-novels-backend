"""create feedback table

Revision ID: 5c29ec878505
Revises: d3f96be3159d
Create Date: 2020-11-16 23:19:52.185384

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey, orm, Table, Text
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


# revision identifiers, used by Alembic.
revision = '5c29ec878505'
down_revision = 'd3f96be3159d'
branch_labels = None
depends_on = None


def upgrade():
    _bind = op.get_bind()
    _session = orm.Session(bind=_bind)

    # Create tables
    op.create_table("feedback",
                    Column("feedback", Integer, primary_key=True),
                    Column("comment", Text),
                    Column("is_active", Boolean, default=True),
                    Column("is_deleted", Boolean, default=False),
                    Column("created_at", DateTime, default=datetime.now()),
                    Column("deleted_at", DateTime, nullable=True)
                    )


def downgrade():
    op.drop_table("feedback")
