"""Migration 2

Revision ID: 6b7a19087deb
Revises: 0117c3816327
Create Date: 2023-03-15 14:21:09.043950

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b7a19087deb'
down_revision = '0117c3816327'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('booking',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userId', sa.String(length=50), nullable=False),
    sa.Column('facilityId', sa.Integer(), nullable=False),
    sa.Column('activityId', sa.Integer(), nullable=False),
    sa.Column('createDate', sa.Date(), nullable=False),
    sa.Column('bookingDate', sa.Date(), nullable=False),
    sa.Column('bookingTime', sa.Time(), nullable=False),
    sa.Column('bookingLength', sa.Time(), nullable=False),
    sa.Column('bookingEndTime', sa.Time(), nullable=False),
    sa.Column('bookingType', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('booking')
    # ### end Alembic commands ###
