"""add job_col_name to GlassbillerDataKey

Revision ID: d30d1d70bb89
Revises: 63d91f3566cb
Create Date: 2024-06-12 16:12:33.455421

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd30d1d70bb89'
down_revision: Union[str, None] = '63d91f3566cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        table_name='data_keys',
        column=sa.Column('job_col_name', sa.String(30))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(
        table_name='data_keys',
        column_name='job_col_name'
    )
    # ### end Alembic commands ###