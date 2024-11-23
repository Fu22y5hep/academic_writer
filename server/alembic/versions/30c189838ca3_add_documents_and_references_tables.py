"""Add documents and references tables

Revision ID: 30c189838ca3
Revises: f24fe58ecd15
Create Date: 2024-11-23 08:53:10.641732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30c189838ca3'
down_revision = 'f24fe58ecd15'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('preferences', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'preferences')
    # ### end Alembic commands ###