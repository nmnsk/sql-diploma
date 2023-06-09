"""1_add_service_models

Revision ID: 1889e38a659f
Revises: 
Create Date: 2023-05-22 11:26:36.529055

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1889e38a659f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('answer_query', sa.Text(), nullable=False),
    sa.Column('check_query', sa.Text(), nullable=True),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('included_keywords', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('excluded_keywords', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('included_keywords_perf', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('excluded_keywords_perf', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('rows_affected', sa.Integer(), nullable=True),
    sa.Column('execution_time', sa.Float(), nullable=True),
    sa.Column('send_hint', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('first_name', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=False),
    sa.Column('patronymic', sa.String(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('solution',
    sa.Column('query', sa.Text(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('verdict', sa.String(length=255), nullable=False),
    sa.Column('verdict_description', sa.Text(), nullable=True),
    sa.Column('rows_affected', sa.Integer(), nullable=True),
    sa.Column('execution_time', sa.Float(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('solution')
    op.drop_table('user')
    op.drop_table('task')
    # ### end Alembic commands ###
