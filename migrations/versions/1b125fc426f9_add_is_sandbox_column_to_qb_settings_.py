"""add is_sandbox column to qb_settings table

Revision ID: 1b125fc426f9
Revises: c81871ef2525
Create Date: 2024-06-17 11:16:55.774328

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b125fc426f9'
down_revision: Union[str, None] = 'c81871ef2525'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('qb_settings', sa.Column('is_sandbox', sa.Boolean(), nullable=False, server_default='true'))


def downgrade() -> None:
    op.drop_column('qb_settings', 'is_sandbox')
