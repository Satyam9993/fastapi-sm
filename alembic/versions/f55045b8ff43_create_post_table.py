"""create post table

Revision ID: f55045b8ff43
Revises: 
Create Date: 2023-04-19 14:38:38.014348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f55045b8ff43'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column('title', sa.String(), nullable=False),

                    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
