"""create qb_settings table

Revision ID: c81871ef2525
Revises: d30d1d70bb89
Create Date: 2024-06-17 11:00:55.679700

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c81871ef2525'
down_revision: Union[str, None] = 'd30d1d70bb89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('qb_settings',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'),nullable=False),
                    sa.Column('client_id', sa.String(length=255), nullable=False),
                    sa.Column('client_secret', sa.String(length=255), nullable=False),
                    sa.Column('refresh_token', sa.String(length=255), nullable=False),
                    sa.Column('access_token', sa.String(length=255), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False, default=sa.func.now()),
                    sa.Column('updated_at', sa.DateTime(), nullable=False, default=sa.func.now()),
                    )


def downgrade() -> None:
    op.drop_table('qb_settings')
