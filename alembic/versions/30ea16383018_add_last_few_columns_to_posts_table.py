"""Add last few columns to posts table

Revision ID: 30ea16383018
Revises: c9b3e1630669
Create Date: 2022-11-19 23:40:11.502868

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30ea16383018'
down_revision = 'c9b3e1630669'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('is_published', sa.Boolean(), server_default='TRUE', nullable=False),)
    op.add_column('posts', sa.Column('rating', sa.Integer(), server_default='0', nullable=False),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
                            
    pass


def downgrade() -> None:
    op.drop_column('posts', 'is_published')
    op.drop_column('posts', 'rating')
    op.drop_column('posts', 'created_at')
    pass
