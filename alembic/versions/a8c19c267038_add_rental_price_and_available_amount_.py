"""add rental price and available amount to movie table

Revision ID: a8c19c267038
Revises: 551b263720b0
Create Date: 2025-08-30 09:18:45.249161

"""
from typing import Sequence, Union

from alembic import op
import sqlmodel as sa


# revision identifiers, used by Alembic.
revision: str = 'a8c19c267038'
down_revision: Union[str, Sequence[str], None] = '551b263720b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('movie', sa.Column('rental_price', sa.Float(), nullable=True))
    op.add_column('movie', sa.Column('available_amount', sa.Integer(), nullable=True))



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('movie', 'rental_price')
    op.drop_column('movie', 'available_amount')
