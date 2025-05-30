"""Refactor transaction_products model

Revision ID: ab772645dabd
Revises: 6c1244745704
Create Date: 2025-04-26 10:56:38.949686

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab772645dabd'
down_revision: Union[str, None] = '6c1244745704'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transaction_products',
    sa.Column('transaction_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['transaction_id'], ['transaction.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('transaction_id', 'product_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction_products')
    # ### end Alembic commands ###
