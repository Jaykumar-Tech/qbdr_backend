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
    total_balance_after_payments_1: Optional[str] = "0"
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
    csvColumns: Optional[str] = "row_number,job_id,status,referral_number,vehicle.vin,consumer.name.last,consumer.name.first,commercialaccount_name,parts,invoice_date,total_materials,total_labor,total_subtotal,total_taxes,total_after_taxes,deductible,total_balance_after_payments,vehicle.year,vehicle.make,vehicle.model,vehicle.sub_model,vehicle.style,insurance_fleet_name,bill_to.consumer_edi.trading_partner"
    csvColumnNames: Optional[str] = "Row #,Job #,Job Type,Referral #,Vin #,Last Name,First Name,Commercial Account Name,Parts,Invoice Date,Materials,Labor,Sub-Total,Sales Tax,Total Invoice,Deductible,Balance Due,Year,Make,Model,Sub-Model,Style,Bill To,Trading Partner"
    csvRow_export: Optional[str] = ""
    csvAllRowsSelected: Optional[str] = "yes"

class DateRangeModel(GlassbillerBase):
    start_date: str
    end_date: Optional[str]