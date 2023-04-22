"""Changed column nameas

Revision ID: d7076e72989c
Revises: e69c60fd5ef7
Create Date: 2023-04-14 13:56:55.253739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7076e72989c'
down_revision = 'e69c60fd5ef7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sales', schema=None) as batch_op:
        batch_op.add_column(sa.Column('saleValue', sa.Float(), nullable=False))
        batch_op.add_column(sa.Column('facilityId', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('activityId', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('saleDate', sa.Date(), nullable=True))
        batch_op.drop_column('Activityid')
        batch_op.drop_column('Facilityid')
        batch_op.drop_column('SaleDate')
        batch_op.drop_column('SaleVal')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sales', schema=None) as batch_op:
        batch_op.add_column(sa.Column('SaleVal', sa.FLOAT(), nullable=False))
        batch_op.add_column(sa.Column('SaleDate', sa.DATE(), nullable=True))
        batch_op.add_column(sa.Column('Facilityid', sa.INTEGER(), nullable=False))
        batch_op.add_column(sa.Column('Activityid', sa.INTEGER(), nullable=False))
        batch_op.drop_column('saleDate')
        batch_op.drop_column('activityId')
        batch_op.drop_column('facilityId')
        batch_op.drop_column('saleValue')

    # ### end Alembic commands ###
