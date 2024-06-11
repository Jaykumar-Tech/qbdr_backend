import time
import requests
from decouple import config
from urllib.parse import urlparse, parse_qs

from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from tools import get_user_id, send_email

from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT, generateJWT, decode_token

from .schema import FiltersModel, SearchPayloadModel, DateRangeModel

router = APIRouter()

@router.get('/get_api_token', dependencies=[Depends(JWTBearer())], tags=["Glassbiller"])
def get_api_token():
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
    
@router.post("/search_payments", dependencies=[Depends(JWTBearer())], tags=["Glassbiller"])
def search_payments(date_range: DateRangeModel, request: Request, db: Session=Depends(get_db)):
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