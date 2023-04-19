"""add column to post table

Revision ID: 1cccf4b8c5b4
Revises: f55045b8ff43
Create Date: 2023-04-19 15:02:14.940707

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cccf4b8c5b4'
down_revision = 'f55045b8ff43'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', column=sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
