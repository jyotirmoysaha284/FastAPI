"""Add users table

Revision ID: fa0dcd4b40cc
Revises: 0629982752b0
Create Date: 2022-11-19 23:02:31.005869

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa0dcd4b40cc'
down_revision = '0629982752b0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False),
                            sa.Column('email', sa.String, nullable=False),
                            sa.Column('password', sa.String, nullable=False),
                            sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                            sa.PrimaryKeyConstraint('id'),
                            sa.UniqueConstraint('email')
                            )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
