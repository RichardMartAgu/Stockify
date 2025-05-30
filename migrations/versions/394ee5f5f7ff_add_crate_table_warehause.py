"""Add crate table warehause

Revision ID: 394ee5f5f7ff
Revises: b9f47bbd22a5
Create Date: 2025-03-15 21:59:29.365528

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '394ee5f5f7ff'
down_revision: Union[str, None] = 'b9f47bbd22a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'warehouse',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('address', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Primero, eliminamos la clave foránea
    op.drop_constraint('warehouse_user_id_fkey', 'warehouse', type_='foreignkey')

    # Después, eliminamos la tabla warehouse
    op.drop_table('warehouse')
    # ### end Alembic commands ###

