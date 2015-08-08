"""empty message

Revision ID: 54435077e60
Revises: None
Create Date: 2015-08-08 08:01:04.365719

"""

# revision identifiers, used by Alembic.
revision = '54435077e60'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('report_settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_url', sa.String(length=100), nullable=False),
    sa.Column('project_name', sa.String(length=100), nullable=False),
    sa.Column('collaboration_type', sa.String(length=100), nullable=False),
    sa.Column('collaboration_project_name', sa.String(length=100), nullable=False),
    sa.Column('start_sprint', sa.Integer(), nullable=False),
    sa.Column('start_day', sa.Integer(), nullable=False),
    sa.Column('start_month', sa.Integer(), nullable=False),
    sa.Column('start_year', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('report_settings')
    ### end Alembic commands ###
