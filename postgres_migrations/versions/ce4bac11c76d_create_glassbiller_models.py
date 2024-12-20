"""create glassbiller models

Revision ID: ce4bac11c76d
Revises: c36e90a7be0c
Create Date: 2024-06-20 17:06:14.012038

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ce4bac11c76d'
down_revision: Union[str, None] = 'c36e90a7be0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'jobs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('job_id', sa.Integer(), nullable=False),
        sa.Column('job_type', sa.String(length=10), nullable=True),
        sa.Column('refferal', sa.Integer(), nullable=True),
        sa.Column('vin', sa.String(length=20), nullable=True),
        sa.Column('first_name', sa.String(length=20), nullable=True),
        sa.Column('last_name', sa.String(length=20), nullable=True),
        sa.Column('commercial_account_name', sa.String(length=80), nullable=True),
        sa.Column('parts', sa.String(length=255), nullable=True),
        sa.Column('invoice_date', sa.Date(), nullable=True),
        sa.Column('materials', sa.Float(), nullable=True, default=0),
        sa.Column('labor', sa.Float(), nullable=True),
        sa.Column('sub_total', sa.Float(), nullable=True),
        sa.Column('sales_tax', sa.Float(), nullable=True),
        sa.Column('total_invoice', sa.Float(), nullable=True),
        sa.Column('deductible', sa.Float(), nullable=True),
        sa.Column('balance_due', sa.Float(), nullable=True),
        sa.Column('year', sa.Integer(), nullable=True),
        sa.Column('make', sa.String(length=30), nullable=True),
        sa.Column('model', sa.String(length=30), nullable=True),
        sa.Column('sub_model', sa.String(length=20), nullable=True),
        sa.Column('style', sa.String(length=30), nullable=True),
        sa.Column('bill_to', sa.String(length=255), nullable=True),
        sa.Column('trading_partner', sa.String(length=80), nullable=True),
        sa.Column('proper_name', sa.String(length=80), nullable=True),
        sa.Column('glass_backglass_replacement', sa.Float(), nullable=True),
        sa.Column('glass_quarterglass_replacement', sa.Float(), nullable=True),
        sa.Column('glass_sidewindow_replacement', sa.Float(), nullable=True),
        sa.Column('glass_windshield_replacement', sa.Float(), nullable=True),
        sa.Column('glass_kit', sa.Float(), nullable=True),
        sa.Column('glass_labor', sa.Float(), nullable=True),
        sa.Column('glass_molding', sa.Float(), nullable=True),
        sa.Column('glass_RandI', sa.Float(), nullable=True),
        sa.Column('adas_dual_recalibration', sa.Float(), nullable=True),
        sa.Column('adas_dynamic_recalibration', sa.Float(), nullable=True),
        sa.Column('adas_static_recalibration', sa.Float(), nullable=True),
        sa.Column('insurance_discounts_deductible', sa.Float(), nullable=True),
        sa.Column('insurance_discounts_adjustment', sa.Float(), nullable=True),
        sa.Column('paid', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table(
        'insurance_rates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('company', sa.String(length=80), nullable=True),
        sa.Column('kit', sa.Float(), nullable=True),
        sa.Column('static', sa.Float(), nullable=True),
        sa.Column('dynamic', sa.Float(), nullable=True),
        sa.Column('dual', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table(
        'data_keys',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('part_no', sa.String(length=80), nullable=True),
        sa.Column('qbo_product_service', sa.String(length=80), nullable=True),
        sa.Column('job_col_name', sa.String(30), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table(
        'qbo_paymentaccounts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('payment_method', sa.String(length=80), nullable=True),
        sa.Column('deposit_account', sa.String(length=80), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create insurance_companies table
    op.create_table(
        'insurance_companies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('trading_partner', sa.String(length=80), nullable=True),
        sa.Column('company_name', sa.String(length=80), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('jobs')
    op.drop_table('insurance_rates')
    op.drop_table('data_keys')
    op.drop_table('insurance_companies')
    op.drop_table('qbo_paymentaccounts')
    # ### end Alembic commands ###
