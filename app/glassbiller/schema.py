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

class JobDetailModel(BaseModel):
    id: int = 0
    job_id: int
    job_type: str
    refferal: Optional[int]
    vin: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    commercial_account_name: Optional[str]
    parts: Optional[str]
    invoice_date: Optional[str]
    materials: Optional[float]
    labor: Optional[float]
    sub_total: Optional[float]
    sales_tax: Optional[float]
    total_invoice: Optional[float]
    deductible: Optional[float]
    balance_due: Optional[float]
    year: Optional[int]
    make: Optional[str]
    model: Optional[str]
    sub_model: Optional[str]
    style: Optional[str]
    bill_to: Optional[str]
    trading_partner: Optional[str]
    proper_name: Optional[str]
    glass_backglass_replacement: Optional[float]
    glass_quarterglass_replacement: Optional[float]
    glass_sidewindow_replacement: Optional[float]
    glass_windshield_replacement: Optional[float]
    glass_kit: Optional[float]
    glass_labor: Optional[float]
    glass_molding: Optional[float]
    glass_RandI: Optional[float]
    adas_dual_recalibration: Optional[float]
    adas_dynamic_recalibration: Optional[float]
    adas_static_recalibration: Optional[float]
    insurance_discounts_deductible: Optional[float]
    insurance_discounts_adjustment: Optional[float]
    paid: Optional[bool]
    created_at: Optional[str]
    updated_at: Optional[str]

class DateRangeModel(GlassbillerBase):
    start_date: str
    end_date: Optional[str]

class InsuranceCompanyModel(BaseModel):
    id: int = 0
    trading_partner: str
    company_name: str
    created_at: Optional[str]
    updated_at: Optional[str]
    
class InsuranceRateModel(BaseModel):
    id: int = 0
    company: str
    kit: Optional[float]
    static: Optional[float]
    dynamic: Optional[float]
    dual: Optional[float]
    created_at: Optional[str]
    updated_at: Optional[str]

class DataKeyModel(BaseModel):
    id: int = 0
    part_no: Optional[str]
    qbo_product_service: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]

class QBOPaymentAccountModel(BaseModel):
    id: int = 0
    payment_method: Optional[str]
    deposit_account: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]