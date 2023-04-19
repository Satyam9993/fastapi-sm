"""add fk to posts tabel

Revision ID: 01a6b14186a0
Revises: 7a568dc6e1dd
Create Date: 2023-04-19 15:28:27.866151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01a6b14186a0'
down_revision = '7a568dc6e1dd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user',sa.Integer() ,nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=['user'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', 'posts')
    op.drop_column('posts', 'user')
    pass
