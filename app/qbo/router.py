import time
import json
import requests
from decouple import config
from urllib.parse import urlparse, parse_qs

from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from tools import get_user_id, send_email

from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT, generateJWT, decode_token

from . import schema as qbSchema
from .repository import QboRepo, QBOController
from app.glassbiller.repository import GlassbillerRepo

router = APIRouter()

@router.get('/get_qbo_settings', dependencies=[Depends(JWTBearer())], tags=["QBO"])
async def get_qbo_settings(request: Request, db: Session = Depends(get_db)):
    user_id = get_user_id(request)
    setting = await QboRepo.get_setting_by_user_id(user_id, db)
    return setting

@router.post('/save_qbo_settings', dependencies=[Depends(JWTBearer())], tags=["QBO"])
async def save_qbo_settings(qbo_settings: qbSchema.QboSetting, request: Request, db: Session = Depends(get_db)):
    user_id = get_user_id(request)
    qbo_settings.update({"user_id": user_id})
    settings = await QboRepo.get_setting_by_user_id(user_id, db)
    if settings == None:
        await QboRepo.create_setting(qbo_settings, db)
    else:
        await QboRepo.update_setting(qbo_settings, db)
    
    return settings

@router.get('/get_authuri', dependencies=[Depends(JWTBearer())], tags=["QBO"])
async def get_authuri(request: Request, db: Session = Depends(get_db)):
    user_id = get_user_id(request)
    qbo_settings = await QboRepo.get_setting_by_user_id(user_id, db)
    if qbo_settings == None:
        raise HTTPException(status_code=403, detail="QBO Settings Not Found!")
    qb_controller = QBOController(
        client_id=qbo_settings.client_id,
        client_secret=qbo_settings.client_secret,
        access_token=qbo_settings.access_token,
        refresh_token=qbo_settings.refresh_token,
        realm_id=qbo_settings.ream_id,
        environment="sandbox" if qbo_settings.is_sandbox else "production",
        redirect_uri="https://glasscleaner.oceanautoglass.net/rediect_url" if qbo_settings.is_sandbox else "http://localhost:3000/rediect_url"
    )
    await qb_controller.init()
    auth_uri = await qb_controller.get_authUri()
    return auth_uri

@router.post('/create_sales_receipt', dependencies=[Depends(JWTBearer())], tags=["QBO"])
async def create_sales_receipt(receipt_data: qbSchema.QboCreateSalesReceipt,request: Request, db: Session = Depends(get_db)):
    try:
        user_id = get_user_id(request)
        qbo_settings = await QboRepo.get_setting_by_user_id(user_id, db)
        if qbo_settings == None:
            raise HTTPException(status_code=403, detail="QBO Settings Not Found!")
        
        insurance_companies = await GlassbillerRepo.get_all_insurance_companies(db)
        payment_accounts = await GlassbillerRepo.get_all_payment_accounts(db)
        
        insurance_companies = { insurance_company.trading_partner: insurance_company.company_name for insurance_company in insurance_companies }
        payment_accounts = { payment_account.payment_method: payment_account.deposit_account for payment_account in payment_accounts }
        
        qb_controller = QBOController(
            client_id=qbo_settings.client_id,
            client_secret=qbo_settings.client_secret,
            access_token=qbo_settings.access_token,
            refresh_token=qbo_settings.refresh_token,
            realm_id=qbo_settings.ream_id,
            environment="sandbox" if qbo_settings.is_sandbox else "production"
        )
        await qb_controller.init()
        receipt_data.billing_data.job_id = f"#{receipt_data.billing_data.job_id}"
        receipt_data.billing_data.refferal = f"#{receipt_data.billing_data.refferal}"
        receipt_data.billing_data.vin = f"#{receipt_data.billing_data.vin}"
        receipt_data.billing_data.year = f"#{receipt_data.billing_data.year}"
        
        new_sales_receipt = await qb_controller.create_sales_receipt(receipt_data.payment_group.to_dict(), receipt_data.billing_data.to_dict, insurance_companies, payment_accounts)
        return new_sales_receipt
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post('/create_payment', dependencies=[Depends(JWTBearer())], tags=["QBO"])
async def create_payment(payment_data: qbSchema.QboCreatePayment,request: Request, db: Session = Depends(get_db)):
    try:
        user_id = get_user_id(request)
        qbo_settings = await QboRepo.get_setting_by_user_id(user_id, db)
        
        if qbo_settings == None:
            raise HTTPException(status_code=400, detail="QBO settings not found")
        
        insurance_companies = await GlassbillerRepo.get_all_insurance_companies(db)
        payment_accounts = await GlassbillerRepo.get_all_payment_accounts(db)
        
        insurance_companies = { insurance_company.trading_partner: insurance_company.company_name for insurance_company in insurance_companies }
        payment_accounts = { payment_account.payment_method: payment_account.deposit_account for payment_account in payment_accounts }
        
        qb_controller = QBOController(
            client_id=qbo_settings.client_id,
            client_secret=qbo_settings.client_secret,
            access_token=qbo_settings.access_token,
            refresh_token=qbo_settings.refresh_token,
            realm_id=qbo_settings.ream_id,
            environment="sandbox" if qbo_settings.is_sandbox else "production"
        )
        await qb_controller.init()
        for billing_data in payment_data.billing_data_list:
            billing_data.job_id = f"#{billing_data.job_id}"
            billing_data.refferal = f"#{billing_data.refferal}"
            billing_data.vin = f"#{billing_data.vin}"
            billing_data.year = f"#{billing_data.year}"
        
        payment_data = payment_data.to_dict()
        new_payment = await qb_controller.create_payment(payment_data["payment_group"], payment_data["billing_data_list"], insurance_companies, payment_accounts)
        return new_payment
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))