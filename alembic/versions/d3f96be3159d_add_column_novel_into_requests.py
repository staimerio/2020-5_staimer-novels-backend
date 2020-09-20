"""add column novel into requests

Revision ID: d3f96be3159d
Revises: 000b9ed704dc
Create Date: 2020-09-20 12:10:45.499343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3f96be3159d'
down_revision = '000b9ed704dc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("requests", sa.Column('novel', sa.Integer,
                                      sa.ForeignKey('novels.novel'))
                  )


def downgrade():
    op.drop_column('requests', 'novel')
