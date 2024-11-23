"""create essay plans table

Revision ID: create_essay_plans
Revises: f4e2159a6d0e
Create Date: 2024-01-09 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'create_essay_plans'
down_revision = 'f4e2159a6d0e'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'essay_plans',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('essay_type', sa.String(), nullable=False),
        sa.Column('topic', sa.String(), nullable=False),
        sa.Column('thesis_statement', sa.String(), nullable=True),
        sa.Column('outline', postgresql.JSONB(), nullable=False),
        sa.Column('guidelines', postgresql.JSONB(), nullable=True),
        sa.Column('word_count_target', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_essay_plans_id'), 'essay_plans', ['id'], unique=False)
    op.create_index(op.f('ix_essay_plans_title'), 'essay_plans', ['title'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_essay_plans_title'), table_name='essay_plans')
    op.drop_index(op.f('ix_essay_plans_id'), table_name='essay_plans')
    op.drop_table('essay_plans')
