"""add glassbiller_product_service

Revision ID: 08ec9a4cf2fa
Revises: 03e35d672ae6
Create Date: 2024-06-26 08:03:20.211688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08ec9a4cf2fa'
down_revision: Union[str, None] = '03e35d672ae6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('data_keys', sa.Column('glassbiller_product_service', sa.String(length=255)))


def downgrade() -> None:
    op.drop_column('data_keys', 'glassbiller_product_service')
