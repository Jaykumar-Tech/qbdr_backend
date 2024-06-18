"""add ream_id column to qb_settings table

Revision ID: bde2f105eb8f
Revises: 1b125fc426f9
Create Date: 2024-06-17 15:01:31.754885

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bde2f105eb8f'
down_revision: Union[str, None] = '1b125fc426f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('qb_settings', sa.Column('ream_id', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('qb_settings','ream_id')
