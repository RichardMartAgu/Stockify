"""Refactor user model stripe_subscription_status: bolean


Revision ID: 0c88ff742791
Revises: cd9002fe3250
Create Date: 2025-05-23 20:31:07.970032

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c88ff742791'
down_revision: Union[str, None] = 'cd9002fe3250'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_stripe_subscription_id_key', 'user', type_='unique')
    op.drop_column('user', 'stripe_subscription_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('stripe_subscription_id', sa.VARCHAR(length=150), autoincrement=False, nullable=True))
    op.create_unique_constraint('user_stripe_subscription_id_key', 'user', ['stripe_subscription_id'])
    # ### end Alembic commands ###
