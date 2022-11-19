"""Add foreign key to posts table

Revision ID: c9b3e1630669
Revises: fa0dcd4b40cc
Create Date: 2022-11-19 23:25:33.457626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9b3e1630669'
down_revision = 'fa0dcd4b40cc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', 
                            local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', column_name='owner_id')
    pass
