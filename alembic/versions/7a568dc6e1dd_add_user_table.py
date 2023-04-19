"""add user table

Revision ID: 7a568dc6e1dd
Revises: 1cccf4b8c5b4
Create Date: 2023-04-19 15:13:34.219291

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a568dc6e1dd'
down_revision = '1cccf4b8c5b4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                             sa.Column('email', sa.String(), nullable=False, unique=True),
                             sa.Column('password', sa.String(), nullable=False),
                             sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False)
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
