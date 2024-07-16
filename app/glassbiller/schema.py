import datetime
from typing import Optional
from pydantic import EmailStr
from pydantic import BaseModel

class GlassbillerBase(BaseModel):
    access_token: str

class FiltersModel(BaseModel):
    all: Optional[str] = ""
    job_id: Optional[str] = ""
    status: Optional[str] = "invoice"
    customer_last_name: Optional[str] = ""
    referral_number: Optional[str] = ""
    customer_first_name: Optional[str] = ""
    parts: Optional[str] = ""
    invoice_date_option: Optional[str] = ""
    range_invoice_date_1: Optional[str] = ""
    range_invoice_date_2: Optional[str] = ""
    total_materials_option: Optional[str] = ""
    total_materials_1: Optional[str] = ""
    total_materials_2: Optional[str] = ""
    total_labor_option: Optional[str] = ""
    total_labor_1: Optional[str] = ""
    total_labor_2: Optional[str] = ""
    total_subtotal_option: Optional[str] = ""
    total_subtotal_1: Optional[str] = ""
    total_subtotal_2: Optional[str] = ""
    total_taxes_option: Optional[str] = ""
    total_taxes_1: Optional[str] = ""
    total_taxes_2: Optional[str] = ""
    total_after_taxes_option: Optional[str] = ""
    total_after_taxes_1: Optional[str] = ""
    total_after_taxes_2: Optional[str] = ""
    deductible_option: Optional[str] = ""
    deductible_1: Optional[str] = ""
    deductible_2: Optional[str] = ""
    total_balance_after_payments_option: Optional[str] = ""
    total_balance_after_payments_1: Optional[str] = ""
    total_balance_after_payments_2: Optional[str] = ""
    commercialaccount_name: Optional[str] = ""
    vehicle_year: Optional[str] = ""
    vehicle_make: Optional[str] = ""
    vehicle_model: Optional[str] = ""
    vehicle_sub_model: Optional[str] = ""
    vehicle_style: Optional[str] = ""
    insurance_fleet_name: Optional[str] = ""
    edi_trading_partner: Optional[str] = ""

class SearchPayloadModel(GlassbillerBase):
    count_only: Optional[str] = "no"
    page: Optional[int] = 1
    limit: Optional[int] = 50
    sortBy: Optional[str] = "install_context"
    sortDesc: Optional[bool] = False
    exportCSV: Optional[str] = "no"
    filters: FiltersModel
    csvColumns: Optional[str] = ""
    csvColumnNames: Optional[str] = ""
    csvRow_export: Optional[str] = ""
    csvAllRowsSelected: Optional[str] = ""

class DateRangeModel(GlassbillerBase):
    start_date: str
    end_date: Optional[str]

class InsuranceCompanyModel(BaseModel):
    id: int = 0
    trading_partner: str
    company_name: str
    created_at: Optional[str]
    updated_at: Optional[str]