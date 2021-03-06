"""empty message

Revision ID: e8d307ccd871
Revises: a6918cbd76f9
Create Date: 2020-05-18 10:20:22.568416

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8d307ccd871'
down_revision = 'a6918cbd76f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('countries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('country_code', sa.String(length=2), nullable=True),
    sa.Column('date', sa.String(length=64), nullable=True),
    sa.Column('cases', sa.String(length=64), nullable=True),
    sa.Column('deaths', sa.String(length=64), nullable=True),
    sa.Column('recovered', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('us_state',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(length=64), nullable=True),
    sa.Column('state', sa.String(length=64), nullable=True),
    sa.Column('positive', sa.String(length=64), nullable=True),
    sa.Column('positive_increase', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('us_state')
    op.drop_table('countries')
    # ### end Alembic commands ###
