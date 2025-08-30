"""update movies table

Revision ID: ad17337e5e79
Revises: 
Create Date: 2025-08-29 16:05:59.447883

"""
from typing import Sequence, Union

from alembic import op
import sqlmodel as sa
# import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad17337e5e79'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('movie', 'year', new_column_name='year_released')
    op.add_column('movie', sa.Column('category', sa.String(length=100), nullable=True))
    op.add_column('movie', sa.Column('rating', sa.Integer(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('movie', 'year_released', new_column_name='year')
    op.drop_column('movie', 'category')
    op.drop_column('movie', 'rating')
