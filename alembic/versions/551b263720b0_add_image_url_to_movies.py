"""add image url to movies

Revision ID: 551b263720b0
Revises: ad17337e5e79
Create Date: 2025-08-29 17:45:48.229214

"""
from typing import Sequence, Union
import sqlmodel as sa

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '551b263720b0'
down_revision: Union[str, Sequence[str], None] = 'ad17337e5e79'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('movie', sa.Column('image_url', sa.String(), nullable=True))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('movie', 'image_url')
    pass
