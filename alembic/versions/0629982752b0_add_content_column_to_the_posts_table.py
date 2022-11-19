"""Add Content column to the posts table

Revision ID: 0629982752b0
Revises: 3aaabc516352
Create Date: 2022-11-19 22:56:12.019244

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0629982752b0'
down_revision = '3aaabc516352'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
