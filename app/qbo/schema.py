import datetime
from typing import Optional, List
from pydantic import EmailStr
from pydantic import BaseModel

class QboSetting(BaseModel):
    id: int
    user_id: int
    client_id: str
    client_secret: str
    access_token: str
    refresh_token: str
    realm_id: str
    is_sandbox: bool
    created_at: str
    updated_at: str

class QboPaymentGroup(BaseModel):
    total_amount: float
    total_payments: int
    id: int
    shop_id: int
    type: str
    date: str
    x_action_type: str
    x_action_number: str
    payment_account_id: str
    created: int
    qbo_account_id: str
    qbo_account_name: str
    qb_exported: int
    customer_name: str
    payment_account_name: str
    
    def to_dict(self):
        return {
            "total_amount": self.total_amount,
            "total_payments": self.total_payments,
            "id": self.id,
            "shop_id": self.shop_id,
            "type": self.type,
            "date": self.date,
            "x_action_type": self.x_action_type,
            "x_action_number": self.x_action_number,
            "payment_account_id": self.payment_account_id,
            "created": self.created,
            "qbo_account_id": self.qbo_account_id,
            "qbo_account_name": self.qbo_account_name,
            "qb_exported": self.qb_exported,
            "customer_name": self.customer_name,
            "payment_account_name": self.payment_account_name
        }

class QboBillingData(BaseModel):
    job_id: int
    refferal: int
    vin: int
    proper_name: str
    trading_partner: str
    year: int
    make: str
    model: str
    glass_backglass_replacement: Optional[float] = 0.0
    glass_quarterglass_replacement: Optional[float] = 0.0
    glass_sidewindow_replacement: Optional[float] = 0.0
    glass_windshield_replacement: Optional[float] = 0.0
    glass_kit: Optional[float] = 0.0
    glass_labor: Optional[float] = 0.0
    glass_molding: Optional[float] = 0.0
    glass_RandI: Optional[float] = 0.0
    adas_dual_recalibration: Optional[float] = 0.0
    adas_dynamic_recalibration: Optional[float] = 0.0
    adas_static_recalibration: Optional[float] = 0.0
    insurance_discounts_deductible: Optional[float] = 0.0
    insurance_discounts_adjustment: Optional[float] = 0.0
    
    def to_dict(self):
        return {
            "Job #": self.job_id,
            "Referral #": self.refferal,
            "Vin #": self.vin,
            "Proper Name": self.proper_name,
            "Trading Partner": self.trading_partner,
            "Year": self.year,
            "Make": self.make,
            "Model": self.model,
            "Glass:Backglass Replacement": self.glass_backglass_replacement,
            "Glass:Quarter glass Replacement": self.glass_quarterglass_replacement,
            "Glass:Side window Replacement": self.glass_sidewindow_replacement,
            "Glass:Windshield Replacement": self.glass_windshield_replacement,
            "Glass:Kit": self.glass_kit,
            "Glass:Labor": self.glass_labor,
            "Glass:Molding": self.glass_molding,
            "Glass:R&I": self.glass_RandI,
            "ADAS:Dual Recalibration": self.adas_dual_recalibration,
            "ADAS:Dynamic Recalibration": self.adas_dynamic_recalibration,
            "ADAS:Static Recalibration": self.adas_static_recalibration,
            "Insurance Discounts:Deductible": self.insurance_discounts_deductible,
            "Insurance Discounts:Adjustment": self.insurance_discounts_adjustment
        }

class QboCreateSalesReceipt(BaseModel):
    payment_group: QboPaymentGroup
    billing_data: QboBillingData
    
    def to_dict(self):
        return {
            "payment_group": self.payment_group.to_dict(),
            "billing_data": self.billing_data.to_dict()
        }

class QboCreatePayment(BaseModel):
    payment_group: QboPaymentGroup
    billing_data_list: List[QboBillingData]
    
    def to_dict(self):
        return {
            "payment_group": self.payment_group.to_dict(),
            "billing_data_list": [billing_data.to_dict() for billing_data in self.billing_data_list]
        }