from sqlalchemy import Column, Integer, String, Boolean, MetaData, Date, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)

class GlassbillerJob(Base):
    __tablename__ = "jobs"
    
    # Original Job Data
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, nullable=False)
    job_type = Column(String(10))
    refferal = Column(Integer)
    vin = Column(String(20))
    first_name = Column(String(20))
    last_name = Column(String(20))
    commercial_account_name = Column(String(80))
    parts = Column(String(255))
    invoice_date = Column(Date)
    materials = Column(Float, default=0)
    labor = Column(Float)
    sub_total = Column(Float)
    sales_tax = Column(Float)
    total_invoice = Column(Float)
    deductible = Column(Float)
    balance_due = Column(Float)
    year = Column(Integer)
    make = Column(String(30))
    model = Column(String(30))
    sub_model = Column(String(20))
    style = Column(String(30))
    bill_to = Column(String(255))
    trading_partner = Column(String(80))
    
    # Parsed Job Data
    proper_name = Column(String(80))
    glass_backglass_replacement = Column(Float)
    glass_quarterglass_replacement = Column(Float)
    glass_sidewindow_replacement = Column(Float)
    glass_windshield_replacement = Column(Float)
    glass_kit = Column(Float)
    glass_labor = Column(Float)
    glass_molding = Column(Float)
    glass_RandI = Column(Float)
    adas_dual_recalibration = Column(Float)
    adas_dynamic_recalibration = Column(Float)
    adas_static_recalibration = Column(Float)
    insurance_discounts_deductible = Column(Float)
    insurance_discounts_adjustment = Column(Float)
    
    paid = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class GlassbillerInsuranceRate(Base):
    __tablename__ = "insurance_rates"
    
    id = Column(Integer, index=True, primary_key=True)
    company = Column(String(80))
    kit = Column(Float)
    static = Column(Float)
    dynamic = Column(Float)
    dual = Column(Float)
    
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class GlassbillerDataKey(Base):
    __tablename__ = "data_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    part_no = Column(String(80))
    qbo_product_service = Column(String(80))
    job_col_name = Column(String(30))
    
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class QBOPaymentAccount(Base):
    __tablename__ = "qbo_paymentaccounts"
    
    id = Column(Integer, primary_key=True, index=True)
    payment_method = Column(String(80))
    deposit_account = Column(String(80))
    
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class InsuranceCompany(Base):
    __tablename__ = "insurance_companies"
    
    id = Column(Integer, primary_key=True, index=True)
    trading_partner = Column(String(80))
    company_name = Column(String(80))
    
    created_at = Column(DateTime)
    updated_at = Column(DateTime)