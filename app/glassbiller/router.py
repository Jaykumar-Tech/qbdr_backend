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

from . import schema as gbSchema
from .repository import GlassbillerRepo

router = APIRouter()

@router.get('/get_api_token', dependencies=[Depends(JWTBearer())], tags=["Glassbiller"])
async def get_api_token():
    try:
        login_detail = requests.post(url="https://auth.glassbiller.com/api/tenant/login",
                                    data={
                                        "u": config("GLASSBILLER_EMAIL"),
                                        "p": config("GLASSBILLER_PASSWORD"),
                                        "tid": "glassbiller-prod"
                                    }).json()

        id_token = login_detail.get("idToken")
        refresh_token = login_detail.get("refreshToken")

        auth_header = {
            "Authorization": f"Bearer {id_token}",
            "Cookie": f"tenant-tid=glassbiller-prod; tenant-token={id_token}; tenant-refresh-token={refresh_token}"
        }

        new_url = requests.get(url="https://auth.glassbiller.com/api/glassbiller/go",
                            headers=auth_header).content

        query_components = parse_qs(urlparse(new_url).query)
        query_components = {key.decode('utf-8'): val[0].decode('utf-8') for key, val in query_components.items()}
        auth_code = query_components['code'] if 'code' in query_components else None
        auth_id = query_components['m'] if 'm' in query_components else None

        if auth_code is None or auth_id is None:
            raise HTTPException(status_code=403, detail="Glassbiller Authentication Failed!")

        response = requests.post("https://auth.glassbiller.com/api/oauth/exchange",
                                data={"t": auth_code, "a": auth_id})
        if response.status_code == 200:
            access_token = response.json().get("access_token")
        else:
            raise HTTPException(status_code=403, detail="Cannot find access token!")
        
        return {
            "access_token": access_token
        }
    except Exception as e:
        print(f"Error occures when get api token: {e}")
        raise HTTPException(status_code=403, detail=str(e))
    
@router.post("/search_payments", dependencies=[Depends(JWTBearer())], tags=["Glassbiller"])
async def search_payments(date_range: gbSchema.DateRangeModel, request: Request, db: Session=Depends(get_db)):
    request_headers = {
        "Authorization": f"Bearer {date_range.access_token}",
        "Content-Type": "application/json;charset=UTF-8",
    }
    
    response = requests.get(url=f"https://uat.glassbiller.com/api/arap/paymentGroups?shopId=2329&dateFrom={date_range.start_date}&dateTo={date_range.end_date}&page=1",
                        headers=request_headers)
    if response.status_code == 200:
        payment_data = []
        pagination_data = response.json().get('pagination')
        page_num = 1
        while(True):
            response = requests.get(url=f"https://uat.glassbiller.com/api/arap/paymentGroups?shopId=2329&dateFrom={date_range.start_date}&dateTo={date_range.end_date}&page={page_num}",
                                    headers=request_headers)
            print(response.url)
            if response.status_code == 200:
                payment_data.extend(response.json().get("data"))
                page_num += 1
            else:
                break
            if page_num > pagination_data.get('total') // pagination_data.get('perPage') + 1:
                break
    else:
        print(response.reason)
        raise HTTPException(status_code=response.status_code, detail=response.reason)

    for payment in payment_data:
        payment_id = payment.get('id')
        response = requests.get(url=f"https://uat.glassbiller.com/api/arap/paymentGroups/{payment_id}",
                                headers=request_headers)
        print(response.url)
        if response.status_code == 200:
            payment_details = response.json()
            payment.update(payment_details)
    
    return payment_data

@router.post("/get_job_detail", dependencies=[Depends(JWTBearer())], tags=["Glassbiller"])
async def get_job_detail(search_param: gbSchema.SearchPayloadModel, request: Request, db: Session=Depends(get_db)):
    request_headers = {
        "Authorization": f"Bearer {search_param.access_token}",
        "Content-Type": "application/json;charset=UTF-8",
    }
    
    url = "https://uat.glassbiller.com/unum/job-details/jobslist/search"
    
    payload = search_param.model_dump()
    response = requests.post(url, data=json.dumps(payload), headers=request_headers)
    if response.status_code == 200:
        result = []
        res_data = response.json().get("rows", [])
        for job in res_data:
            csv_job = await GlassbillerRepo.parse_job_data(db, job, search_param.access_token)
            db_job = await GlassbillerRepo.get_job_by_jobid(db, csv_job["Job #"])
            if db_job:
                await GlassbillerRepo.update_job(db, db_job.id, csv_job)
                result.append(csv_job)
            else:
                new_job = await GlassbillerRepo.create_job(db, csv_job)
                if new_job:
                    result.append(csv_job)
            if csv_job['Insurance Discounts:Deductible']:
                deduct_job = {}
                for key in ["Job #", "Last Name", "First Name", "Invoice Date", "Deductible", "Proper Name"]:
                    deduct_job[key] = csv_job[key]
                deduct_job["Insurance Discounts:Deductible"] = -csv_job["Insurance Discounts:Deductible"]
                
                deductible_job = await GlassbillerRepo.get_job_by_jobid(db, deduct_job["Job #"], True)
                if deductible_job:
                    await GlassbillerRepo.update_job(db, deductible_job.id, deduct_job)
                    result.append(deduct_job)
                else:
                    new_deductible_job = await GlassbillerRepo.create_job(db, deduct_job)
                    if new_deductible_job:
                        result.append(deduct_job)
        return result
    else:
        print(response.reason)
        raise HTTPException(status_code=response.status_code, detail=response.reason)

@router.get("/get_data_keys", dependencies=[Depends(JWTBearer())], tags=["Glassbiller"])
async def get_data_keys(request: Request, db: Session=Depends(get_db)):
    user_id = get_user_id(request)
    
    data_keys = await GlassbillerRepo.get_all_data_keys(db)
    
    return {
        "data_keys": data_keys
    }

@router.get("/get_insurance_companies", dependencies=[Depends(JWTBearer())], tags=["Glassbiller"])
async def get_insurance_companies(request: Request, db: Session=Depends(get_db)):
    user_id = get_user_id(request)

    insurance_companies = await GlassbillerRepo.get_all_insurance_companies(db)

    return {
        "insurance_companies": insurance_companies
    }

@router.post("/update_insurance_company", dependencies=[Depends(JWTBearer())], tags=["Glassbiller"])
async def update_insurance_company(insurance_company: gbSchema.InsuranceCompanyModel, request: Request, db: Session=Depends(get_db)):
    user_id = get_user_id(request)
    insurance_company = await GlassbillerRepo.update_insurance_company(db, insurance_company.model_dump())
    if insurance_company:
        return {
            "insurance_company": insurance_company
        }
    else:
        raise HTTPException(status_code=400, detail="Update Insurance company Failed!")

@router.get("/delete_insurance_company/{id}", dependencies=[Depends(JWTBearer())], tags=["Glassbiller"])
async def delete_insurance_company(id: int, request: Request, db: Session=Depends(get_db)):
    user_id = get_user_id(request)
    insurance_company = await GlassbillerRepo.delete_insurance_company(db, id)
    if insurance_company:
        return "success"
    else:
        raise HTTPException(status_code=400, detail="Delete Insurance company Failed!")

@router.get("/get_insurance_rates", dependencies=[Depends(JWTBearer())], tags=["Glassbiller"])
async def get_insurance_rates(request: Request, db: Session=Depends(get_db)):
    user_id = get_user_id(request)
    
    insurance_rates = await GlassbillerRepo.get_all_insurance_rates(db)
    if insurance_rates:
        return {
            "insurance_rates": insurance_rates
        }
    else:
        raise HTTPException(status_code=400, detail="Get Insurance Rates Failed!")

@router.post("/update_insurance_rates", dependencies=[Depends(JWTBearer())], tags=["Glassbiller"])
async def update_insurance_rates(insurance_rate: gbSchema.InsuranceRateModel, request: Request, db: Session=Depends(get_db)):
    user_id = get_user_id(request)
    insurance_rate = await GlassbillerRepo.update_insurance_rates(db, insurance_rate.model_dump())
    if insurance_rate:
        return {
            "insurance_rate": insurance_rate
        }
    else:
        raise HTTPException(status_code=400, detail="Update Insurance Rate Failed!")

@router.get("/delete_insurance_rates/{id}", dependencies=[Depends(JWTBearer())], tags=["Glassbiller"])
async def delete_insurance_rates(id: int, request: Request, db: Session=Depends(get_db)):
    user_id = get_user_id(request)
    insurance_rate = await GlassbillerRepo.delete_insurance_rates(db, id)
    if insurance_rate:
        return "success"
    else:
        raise HTTPException(status_code=400, detail="Delete Insurance Rate Failed!")

@router.get("/get_qbo_payment_accounts", dependencies=[Depends(JWTBearer())], tags=["Glassbiller"])
async def get_qbo_payment_accounts(request: Request, db: Session=Depends(get_db)):
    user_id = get_user_id(request)

    qbo_payment_accounts = await GlassbillerRepo.get_all_qbo_payment_accounts(db)

    return {
        "qbo_payment_accounts": qbo_payment_accounts
    }