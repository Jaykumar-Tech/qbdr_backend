from decouple import config

from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from tools import get_user_id

from app.auth.auth_bearer import JWTBearer

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
    try:
        user_id = get_user_id(request)
        qbo_settings.user_id = user_id
        qb_controller = QBOController(
            client_id=qbo_settings.client_id,
            client_secret=qbo_settings.client_secret,
            environment="sandbox" if qbo_settings.is_sandbox else "production",
            redirect_uri=config("QBO_OAUTH_REDIRECT_URL")
        )
        await qb_controller.init()
        qb_controller.auth_client.get_bearer_token(qbo_settings.auth_code, qbo_settings.realm_id)
        qbo_settings.access_token = qb_controller.auth_client.access_token
        qbo_settings.refresh_token = qb_controller.auth_client.refresh_token
        qbo_settings.realm_id = qb_controller.auth_client.realm_id
        print(qb_controller.auth_client.realm_id)
        settings = await QboRepo.get_setting_by_user_id(user_id, db)
        if settings == None:
            await QboRepo.create_setting(qbo_settings, db)
        else:
            updated_setting = {
                "id": settings.id,
                "client_id": qbo_settings.client_id,
                "client_secret": qbo_settings.client_secret,
                "access_token": qbo_settings.access_token,
                "refresh_token": qbo_settings.refresh_token,
                "realm_id": qbo_settings.realm_id,
                "is_sandbox": qbo_settings.is_sandbox
            }
            await QboRepo.update_setting(updated_setting, db)
        
        return settings
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

@router.post('/get_authuri', dependencies=[Depends(JWTBearer())], tags=["QBO"])
async def get_authuri(qb_settings: qbSchema.QboSetting, request: Request, db: Session = Depends(get_db)):
    user_id = get_user_id(request)
    qbo_settings = await QboRepo.get_setting_by_user_id(user_id, db)
    if qbo_settings == None:
        qb_controller = QBOController(
            client_id=qb_settings.client_id,
            client_secret=qb_settings.client_secret,
            environment="sandbox" if qb_settings.is_sandbox else "production",
            redirect_uri=config("QBO_OAUTH_REDIRECT_URL")
        )
    else:
        qb_controller = QBOController(
            client_id=qbo_settings.client_id,
            client_secret=qbo_settings.client_secret,
            access_token=qbo_settings.access_token,
            refresh_token=qbo_settings.refresh_token,
            realm_id=qbo_settings.realm_id,
            environment="sandbox" if qbo_settings.is_sandbox else "production",
            redirect_uri=config("QBO_OAUTH_REDIRECT_URL")
        )
    await qb_controller.init()
    auth_uri = await qb_controller.get_authUri()
    print(auth_uri)
    return {"auth_uri": auth_uri}

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
        print(f"Insurance Companies: {insurance_companies}")
        payment_accounts = { payment_account.payment_method: payment_account.deposit_account for payment_account in payment_accounts }
        print(f"Payment Accounts: {payment_accounts}")
        
        qb_controller = QBOController(
            client_id=qbo_settings.client_id,
            client_secret=qbo_settings.client_secret,
            access_token=qbo_settings.access_token,
            refresh_token=qbo_settings.refresh_token,
            realm_id=qbo_settings.realm_id,
            environment="sandbox" if qbo_settings.is_sandbox else "production"
        )
        await qb_controller.init()        
        receipt_data.billing_data.job_id = f"#{receipt_data.billing_data.job_id}"
        receipt_data.billing_data.refferal = f"#{receipt_data.billing_data.refferal}"
        receipt_data.billing_data.vin = f"#{receipt_data.billing_data.vin}"
        receipt_data.billing_data.year = f"#{receipt_data.billing_data.year}"
        
        new_sales_receipt = await qb_controller.create_sales_receipt(receipt_data.payment_group.to_dict(), receipt_data.billing_data.to_dict(), insurance_companies, payment_accounts)
        return new_sales_receipt
    except Exception as e:
        updated_settings = {
            "id":qbo_settings.id,
            "client_id":qb_controller.auth_client.client_id,
            "client_secret":qb_controller.auth_client.client_secret,
            "access_token":qb_controller.auth_client.access_token,
            "refresh_token":qb_controller.auth_client.refresh_token,
            "realm_id":qb_controller.realm_id,
        }
        await QboRepo.update_setting(updated_settings, db)
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
            realm_id=qbo_settings.realm_id,
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
        updated_settings = {
            "id":qbo_settings.id,
            "client_id":qb_controller.auth_client.client_id,
            "client_secret":qb_controller.auth_client.client_secret,
            "access_token":qb_controller.auth_client.access_token,
            "refresh_token":qb_controller.auth_client.refresh_token,
            "realm_id":qb_controller.realm_id,
        }
        await QboRepo.update_setting(updated_settings, db)
        raise HTTPException(status_code=400, detail=str(e))

@router.post('/export_to_qbo', dependencies=[Depends(JWTBearer())], tags=["QBO"])
async def export_to_qbo(payment_data: qbSchema.QboPaymentGroup, request: Request, db: Session = Depends(get_db)):
    try:
        user_id = get_user_id(request)
        qbo_settings = await QboRepo.get_setting_by_user_id(user_id, db)

        if qbo_settings == None:
            raise HTTPException(status_code=400, detail="QBO settings not found")

        qb_controller = QBOController(
            client_id=qbo_settings.client_id,
            client_secret=qbo_settings.client_secret,
            access_token=qbo_settings.access_token,
            refresh_token=qbo_settings.refresh_token,
            realm_id=qbo_settings.realm_id,
            environment="sandbox" if qbo_settings.is_sandbox else "production"
        )
        await qb_controller.init()
        
        data_keys = await GlassbillerRepo.get_all_data_keys(db)
        
        insurance_companies = await GlassbillerRepo.get_all_insurance_companies(db)
        payment_accounts = await GlassbillerRepo.get_all_payment_accounts(db)
        
        insurance_companies = { insurance_company.trading_partner: insurance_company.company_name for insurance_company in insurance_companies }
        payment_accounts = { payment_account.payment_method: payment_account.deposit_account for payment_account in payment_accounts }
        
        if len(payment_data.payments) == 0:
            raise HTTPException(status_code=400, detail="Payment data is empty")
        if len(payment_data.payments) == 1:
            payment = payment_data.payments[0]
            result_job = None
            db_job = await GlassbillerRepo.get_job_by_jobid(db, payment.job_id)
            if db_job == None:
                raise HTTPException(status_code=400, detail="Job not found")
            if db_job.paid:
                raise HTTPException(status_code=400, detail="Job is already paid")
            
            if db_job.trading_partner in [None, ""]:
                result_job = await GlassbillerRepo.get_job_by_jobid(db, payment.job_id)
            else:
                if db_job.deductible in [None, 0, "0", ""]:
                    result_job = await GlassbillerRepo.get_job_by_jobid(db, payment.job_id)
                else:
                    if payment.company_name in ["", None]:
                        result_job = await GlassbillerRepo.get_job_by_jobid(db, payment.job_id, is_deductible=True)
                    else:
                        result_job = await GlassbillerRepo.get_job_by_jobid(db, payment.job_id)
            print(result_job.job_id)
            billing_data = {data_key.qbo_product_service: getattr(result_job, data_key.job_col_name) for data_key in data_keys}
            billing_data.update({
                "Job #": f'#{result_job.job_id}',
                "Referral #": f'#{result_job.refferal}',
                "Vin #": f'#{result_job.vin}',
                "Proper Name": result_job.proper_name,
                "Trading Partner": result_job.trading_partner,
                "Year": f'#{result_job.year}',
                "Make": result_job.make,
                "Model": f'#{result_job.model}',
                "Sales Tax": result_job.sales_tax,
            })
            
            billing_amount = 0
            for value in billing_data.values():
                try:
                    billing_amount += float(value)
                except:
                    continue

            if round(billing_amount, 2) > round(payment.amount, 2):
                new_payment = await qb_controller.create_payment(payment_data.model_dump(), [billing_data], insurance_companies, payment_accounts)
                return new_payment
            else:
                new_sales_reciept = await qb_controller.create_sales_receipt(payment_data.model_dump(), billing_data, insurance_companies, payment_accounts)
                return new_sales_reciept
                        
        elif len(payment_data.payments) > 1:
            billing_data_list = []
            for payment in payment_data.payments:
                result_job = None
                db_job = await GlassbillerRepo.get_job_by_jobid(db, payment.job_id)
                if db_job == None:
                    raise HTTPException(status_code=400, detail="Job not found")
                if db_job.paid:
                    raise HTTPException(status_code=400, detail="Job is already paid")
                
                if db_job.trading_partner in [None, ""]:
                    result_job = await GlassbillerRepo.get_job_by_jobid(db, payment.job_id)
                else:
                    if db_job.deductible in [None, 0, "0", ""]:
                        result_job = await GlassbillerRepo.get_job_by_jobid(db, payment.job_id)
                    else:
                        if payment.company_name in ["", None]:
                            result_job = await GlassbillerRepo.get_job_by_jobid(db, payment.job_id, is_deductible=True)
                        else:
                            result_job = await GlassbillerRepo.get_job_by_jobid(db, payment.job_id)
                
                billing_data = {data_key.qbo_product_service: getattr(result_job, data_key.job_col_name) for data_key in data_keys}
                billing_data.update({
                    "Job #": f'#{result_job.job_id}',
                    "Referral #": f'#{result_job.refferal}',
                    "Vin #": f'#{result_job.vin}',
                    "Proper Name": result_job.proper_name,
                    "Trading Partner": result_job.trading_partner,
                    "Year": f'#{result_job.year}',
                    "Make": result_job.make,
                    "Model": f'#{result_job.model}',
                    "Sales Tax": result_job.sales_tax,
                })
                
                billing_data_list.append(billing_data)
                
            if len(billing_data_list) == 0:
                raise HTTPException(status_code=400, detail="No jobs found")
            
            new_payment = await qb_controller.create_payment(payment_data.model_dump(), billing_data_list, insurance_companies, payment_accounts)                
        
    except Exception as e:
        updated_settings = {
            "id":qbo_settings.id,
            "client_id":qb_controller.auth_client.client_id,
            "client_secret":qb_controller.auth_client.client_secret,
            "access_token":qb_controller.auth_client.access_token,
            "refresh_token":qb_controller.auth_client.refresh_token,
            "realm_id":qb_controller.realm_id,
        }
        await QboRepo.update_setting(updated_settings, db)
        raise HTTPException(status_code=400, detail=str(e))
        