import re
from sqlalchemy import extract, or_, and_
from sqlalchemy.orm import Session
from . import model, schema
import datetime
import requests
import json

from tools import get_nested_value
class GlassbillerRepo:

    async def create_job(db: Session, row_data: dict):
        try:
            now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
            new_job = model.GlassbillerJob(
                job_id = row_data.get("Job #", None),
                job_type = row_data.get("Job Type", None),
                refferal = row_data.get("Referral #", None),
                vin = row_data.get("Vin #", None),
                first_name = row_data.get("First Name", None),
                last_name = row_data.get("Last Name", None),
                commercial_account_name = row_data.get("Commercial Account Name", None),
                parts = row_data.get("Parts", None),
                invoice_date = row_data.get("Invoice Date", None),
                materials = row_data.get("Materials", None),
                labor = row_data.get("Labor", None),
                sub_total = row_data.get("Sub-Total", None),
                sales_tax = row_data.get("Sales Tax", None),
                total_invoice = row_data.get("Total Invoice", None),
                deductible = row_data.get("Deductible", None),
                balance_due = row_data.get("Balance Due", None),
                year = row_data.get("Year", None),
                make = row_data.get("Make", None),
                model = row_data.get("Model", None),
                sub_model = row_data.get("Sub-Model", None),
                style = row_data.get("Style", None),
                bill_to = row_data.get("Bill To", None),
                trading_partner = row_data.get("Trading Partner", None),
                proper_name = row_data.get("Proper Name", None),
                glass_backglass_replacement = row_data.get("Glass:Backglass Replacement", None),
                glass_quarterglass_replacement = row_data.get("Glass:Quarter glass Replacement", None),
                glass_sidewindow_replacement = row_data.get("Glass:Side window Replacement", None),
                glass_windshield_replacement = row_data.get("Glass:Windshield Replacement", None),
                glass_kit = row_data.get("Glass:Kit", None),
                glass_labor = row_data.get("Glass:Labor", None),
                glass_molding = row_data.get("Glass:Molding", None),
                glass_RandI = row_data.get("Glass:R&I", None),
                adas_dual_recalibration = row_data.get("ADAS:Dual Recalibration", None),
                adas_dynamic_recalibration = row_data.get("ADAS:Dynamic Recalibration", None),
                adas_static_recalibration = row_data.get("ADAS:Static Recalibration", None),
                insurance_discounts_deductible = row_data.get("Insurance Discounts:Deductible", None),
                insurance_discounts_adjustment = row_data.get("Insurance Discounts:Adjustment", None),
                paid = False,
                created_at = now,
                updated_at = now
            )
            
            db.add(new_job)
            db.commit()
            db.refresh(new_job)
            return new_job
        except Exception as e:
            print(f"Error occures when create new job: {e}")
            db.rollback()
            return None
    
    async def update_job(db: Session, id: str, row_data: dict):
        try:
            now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
            job = db.query(model.GlassbillerJob).filter(model.GlassbillerJob.id == id).first()
            for key, value in row_data.items():
                setattr(job, key, value)
            setattr(job, "updated_at", now)
            db.commit()
            db.refresh(job)
            return job
        except Exception as e:
            print(f"Error occures when update job: {e}")
            db.rollback()
            return None
    
    async def update_job_with_deductible(db: Session, job_id, row_data: dict):
        try:
            now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
            jobs = db.query(model.GlassbillerJob).filter(model.GlassbillerJob.job_id == job_id).all()
            if len(jobs) == 0:
                return None
            elif len(jobs) == 1:
                job = jobs[0]
                for key, value in row_data.items():
                    setattr(job, key, value)
                setattr(job, "updated_at", now)
                db.commit()
                db.refresh(job)
                return job
            else:
                if float(row_data.get("insurance_discounts_deductible", None)) < 0:
                    query = db.query(model.GlassbillerJob).filter(and_(model.GlassbillerJob.job_id == job_id,
                                                                  or_(model.GlassbillerJob.deductible == None,
                                                                      model.GlassbillerJob.deductible == 0,
                                                                      model.GlassbillerJob.deductible == '0',
                                                                      model.GlassbillerJob.insurance_discounts_deductible < 0)))
                else:
                    query = db.query(model.GlassbillerJob).filter(and_(model.GlassbillerJob.job_id == job_id,
                                                                  model.GlassbillerJob.insurance_discounts_deductible > 0))
                db_job = query.first()
                for key, value in row_data.items():
                    setattr(db_job, key, value)
                setattr(db_job, "updated_at", now)
                db.commit()
                db.refresh(db_job)
                return db_job
        except Exception as e:
            print(f"Error occures when update job: {e}")
            db.rollback()
            return None
    
    async def get_job_by_jobid(db: Session, job_id: int, is_deductible: bool=False):
        try:
            if is_deductible == True:
                query = db.query(model.GlassbillerJob).filter(and_(model.GlassbillerJob.job_id == job_id,
                                                                  model.GlassbillerJob.insurance_discounts_deductible > 0))
            else:
                query = db.query(model.GlassbillerJob).filter(and_(model.GlassbillerJob.job_id == job_id,
                                                                  or_(model.GlassbillerJob.deductible == None,
                                                                      model.GlassbillerJob.deductible == 0,
                                                                      model.GlassbillerJob.deductible == '0',
                                                                      model.GlassbillerJob.insurance_discounts_deductible < 0)))
            db_job = query.first()
            return db_job
        except Exception as e:
            print(f"Error occures when get job by jobid: {e}")
            db.rollback()
            return None
    
    async def get_all_payment_accounts(db: Session):
        try:
            return db.query(model.QBOPaymentAccount).all()
        except Exception as e:
            print(f"Error occures when get all payment account: {e}")
            db.rollback()
            return None
    
    async def get_all_insurance_companies(db: Session):
        try:
            return db.query(model.InsuranceCompany).all()
        except Exception as e:
            print(f"Error occures when get all insurance companies: {e}")
            db.rollback()
    
    async def delete_insurance_company(db: Session, id: int):
        try:
            insurance_company = db.query(model.InsuranceCompany).filter(model.InsuranceCompany.id == id).first()
            if insurance_company:
                db.delete(insurance_company)
                db.commit()
                return True
            else:
                return False
        except Exception as e:
            print(f"Error occures when delete insurance company: {e}")
            db.rollback()
            return False
            
    async def update_insurance_company(db: Session, row_data: dict):
        try:
            now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
            insurance_company = db.query(model.InsuranceCompany).filter(model.InsuranceCompany.id == row_data["id"]).first()
            if insurance_company:
                for key, value in row_data.items():
                    if key != "id":
                        setattr(insurance_company, key, value)
                setattr(insurance_company, "updated_at", now)
                db.commit()
                db.refresh(insurance_company)
            else:
                insurance_company = model.InsuranceCompany(
                    id = row_data["id"],
                    trading_partner = row_data.get("trading_partner", None),
                    company_name = row_data.get("company_name", None),
                    created_at = now,
                    updated_at = now
                )

                db.add(insurance_company)
                db.commit()
                db.refresh(insurance_company)
            return insurance_company
        except Exception as e:
            print(f"Error occures when update insurance company: {e}")
            db.rollback()
            return None
    
    async def get_all_data_keys(db: Session):
        try:
            return db.query(model.GlassbillerDataKey).all()
        except Exception as e:
            print(f"Error occures when get all data keys: {e}")
            db.rollback()
            return None
    
    async def update_data_keys(db: Session, row_data: dict):
        try:
            now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
            data_key = db.query(model.GlassbillerDataKey).filter(model.GlassbillerDataKey.id == row_data["id"]).first()
            if data_key:
                for key, value in row_data.items():
                    if key != "id":
                        setattr(data_key, key, value)
                setattr(data_key, "updated_at", now)
                db.commit()
                db.refresh(data_key)
            else:
                data_key = model.GlassbillerDataKey(
                    id = row_data["id"],
                    part_no = row_data.get("part_no", None),
                    qbo_product_service = row_data.get("qbo_product_service", None),
                    job_col_name = row_data.get("job_col_name", None),
                    glassbiller_product_service = row_data.get("glassbiller_product_service", None),
                    created_at = now,
                    updated_at = now
                )
                db.add(data_key)
                db.commit()
                db.refresh(data_key)
            return data_key
        except Exception as e:
            print(f"Error occures when update data keys: {e}")
            db.rollback()
            return None
    
    async def delete_data_keys(db: Session, id: int):
        try:
            data_key = db.query(model.GlassbillerDataKey).filter(model.GlassbillerDataKey.id == id).first()
            if data_key:
                db.delete(data_key)
                db.commit()
                return True
            else:
                return False
        except Exception as e:
            print(f"Error occures when delete data keys: {e}")
            db.rollback()
            return False
    
    async def get_all_insurance_rates(db: Session):
        try:
            return db.query(model.GlassbillerInsuranceRate).all()
        except Exception as e:
            print(f"Error occures when get all insurance rates: {e}")
            db.rollback()
            return None
    
    async def update_insurance_rates(db: Session, row_data: dict):
        try:
            now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
            insurance_rate = db.query(model.GlassbillerInsuranceRate).filter(model.GlassbillerInsuranceRate.id == row_data["id"]).first()
            if insurance_rate:
                for key, value in row_data.items():
                    if key != "id":
                        setattr(insurance_rate, key, value)
                setattr(insurance_rate, "updated_at", now)
                db.commit()
                db.refresh(insurance_rate)
            else:
                insurance_rate = model.GlassbillerInsuranceRate(
                    id = row_data["id"],
                    company = row_data.get("company", None),
                    kit = row_data.get("kit", None),
                    static = row_data.get("static", None),
                    dynamic = row_data.get("dynamic", None),
                    dual = row_data.get("dual", None),
                    created_at = now,
                    updated_at = now
                )
                db.add(insurance_rate)
                db.commit()
                db.refresh(insurance_rate)
            return insurance_rate
        except Exception as e:
            print(f"Error occures when update insurance rates: {e}")
            db.rollback()
            return None
    
    async def delete_insurance_rates(db: Session, id: int):
        try:
            insurance_rate = db.query(model.GlassbillerInsuranceRate).filter(model.GlassbillerInsuranceRate.id == id).first()
            if insurance_rate:
                db.delete(insurance_rate)
                db.commit()
                return True
            else:
                return False
        except Exception as e:
            print(f"Error occures when delete insurance rates: {e}")
            db.rollback()
            return False
    
    async def get_all_qbo_payment_accounts(db: Session):
        try:
            return db.query(model.QBOPaymentAccount).all()
        except Exception as e:
            print(f"Error occures when get all qbo payment accounts: {e}")
            db.rollback()
            return None
    
    async def update_qbo_payment_accounts(db: Session, row_data: dict):
        try:
            now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
            qbo_payment_account = db.query(model.QBOPaymentAccount).filter(model.QBOPaymentAccount.id == row_data["id"]).first()
            if qbo_payment_account:
                for key, value in row_data.items():
                    if key != "id":
                        setattr(qbo_payment_account, key, value)
                setattr(qbo_payment_account, "updated_at", now)
                db.commit()
                db.refresh(qbo_payment_account)
            else:
                qbo_payment_account = model.QBOPaymentAccount(
                    id = row_data["id"],
                    payment_method = row_data.get("payment_method", None),
                    deposit_account = row_data.get("deposit_account", None),
                    created_at = now,
                    updated_at = now
                )
                db.add(qbo_payment_account)
                db.commit()
                db.refresh(qbo_payment_account)
            return qbo_payment_account
        except Exception as e:
            print(f"Error occures when update qbo payment accounts: {e}")
            db.rollback()
            return None
    
    async def delete_qbo_payment_accounts(db: Session, id: int):
        try:
            qbo_payment_account = db.query(model.QBOPaymentAccount).filter(model.QBOPaymentAccount.id == id).first()
            if qbo_payment_account:
                db.delete(qbo_payment_account)
                db.commit()
                return True
            else:
                return False
        except Exception as e:
            print(f"Error occures when delete qbo payment accounts: {e}")
            db.rollback()
            return False
    
    async def parse_job_data(db: Session, job_data: dict, access_token: str) -> dict:
        csvColumns = "job_id,status,referral_number,vehicle.vin,consumer.name.last,consumer.name.first,commercialaccount_name,parts,invoice_date,total_materials,total_labor,total_subtotal,total_taxes,total_after_taxes,deductible,total_balance_after_payments,vehicle.year,vehicle.make,vehicle.model,vehicle.sub_model,vehicle.style,insurance_fleet_name,bill_to.consumer_edi.trading_partner"
        csvColumnNames = "Job #,Job Type,Referral #,Vin #,Last Name,First Name,Commercial Account Name,Parts,Invoice Date,Materials,Labor,Sub-Total,Sales Tax,Total Invoice,Deductible,Balance Due,Year,Make,Model,Sub-Model,Style,Bill To,Trading Partner"
        
        row_data = {}
        for col_name, key in zip(csvColumnNames.split(","), csvColumns.split(",")):
            row_data[col_name] = await get_nested_value(job_data, key)
        
        insurance_rate = db.query(
            model.GlassbillerInsuranceRate
        ).filter(
            model.GlassbillerInsuranceRate.company == row_data["Bill To"]
        ).first()
        
        data_keys = db.query(
            model.GlassbillerDataKey
        ).all()
        
        for part in row_data["Parts"]:
            for key in data_keys:
                row_data.update({
                    key.qbo_product_service: None
                })
                if key.part_no in ["FW", "DW", "FB", "DB", "FD", "DD", "FQ", "DQ", "FV", "DV"]:
                    if key.part_no in part["part_number"][0:2]:
                        part["data_key"] = key
                else:
                    if key.part_no in part["part_number"]:
                        part["data_key"] = key
        
        material_field = []
        for part in row_data["Parts"]:
            if part.get("data_key", None) == None:
                continue
            if part["data_key"].part_no in ["FW", "DW", "FB", "DB", "FD", "DD", "FQ", "DQ", "FV", "DV"]:
                row_data.update({ part["data_key"].qbo_product_service: round(float(row_data["Materials"]), 2) })
                row_data.update({ "Glass:Labor": round(float(row_data["Labor"]), 2) })
                material_field.append(part["data_key"].qbo_product_service)
        
        if len(material_field) == 0:
            for part in row_data["Parts"]:
                if part.get("data_key", None) == None:
                    for key in data_keys:
                        if key.part_no in ["FW", "DW", "FB", "DB", "FD", "DD", "FQ", "DQ", "FV", "DV"] and key.glassbiller_product_service in part["description"]:
                            material_field.append(key.qbo_product_service)
            material_field = material_field[0] if len(material_field) > 0 else "Glass:Windshield Replacement"
            row_data.update({ material_field: round(float(row_data["Materials"]), 2) })
            row_data.update({ "Glass:Labor": round(float(row_data["Labor"]), 2) })
        
        elif len(material_field) == 1:
            material_field = material_field[0]
        
        elif len(material_field) > 1:
            request_headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json;charset=UTF-8",
            }
            job_detail_url = "https://uat.glassbiller.com/apollo/job-details"
            job_detail_payload = {
                "operationName": "getJobParts",
                "variables": {
                    "id": str(row_data["Job #"])
                },
                "query": "query getJobParts($id: ID!, $draft_id: ID) {\n  jobParts(id: $id, draft_id: $draft_id) {\n    ...PartFields\n    __typename\n  }\n}\n\nfragment PartFields on Part {\n  cost\n  description\n  discount\n  hours\n  id\n  is_adhesive_kit_part\n  is_chip\n  is_custom_part\n  is_glass\n  is_inventory_part\n  is_oem\n  is_premium\n  is_recal\n  item_id\n  labor_price\n  list_price\n  materials_price\n  moulding_discount\n  nagsid\n  order\n  order_status\n  part_number\n  po_quantity\n  quantity\n  shop_id\n  total_price\n  flat\n  glaxis_order_item_id\n  pilkington_order_item_id\n  american_order_item_id\n  __typename\n}\n"
            }
            response = requests.post(url=job_detail_url, data=json.dumps(job_detail_payload), headers=request_headers)
            if response.status_code == 200:
                job_part_data = response.json().get("data", {}).get("jobParts", [])
                print(f"Job Part Data: {job_part_data}")
                part_nos = []
                for part in row_data["Parts"]:
                    if part.get("data_key", None) == None:
                        continue
                    for mat in material_field:
                        if part["data_key"].qbo_product_service == mat:
                            part_nos.append((part["part_number"], mat))
                print(f"Part Nos: {part_nos}")
                for job_part in job_part_data:
                    for part_no in part_nos:
                        if job_part["part_number"] == part_no[0]:
                            row_data.update({ part_no[1]: round(float(job_part["materials_price"]), 2) })
            else:
                print(f"Error: {response.text}")
            material_field = material_field[0]
        print(f"Material Field: {material_field}")
        for part in row_data["Parts"]:
            if part.get("data_key", None) == None:
                continue
            if part["data_key"].part_no in ["HAH000448", "HAH200448", "HAH"] and insurance_rate:
                row_data.update({ part["data_key"].qbo_product_service: round(float(insurance_rate.kit), 2) })
                row_data.update({ material_field: round(float(row_data[material_field]) - float(insurance_rate.kit), 2) })
        
        for part in row_data["Parts"]:
            if part.get("data_key", None) == None:
                continue
            if part["data_key"].part_no in ["RECAL STATIC", "RECAL DYNAMIC", "RECAL DUALMETHOD", "RECAL-RTL-STATIC", "RECAL-RTL-DYNAMIC", "RECAL-RTL-BOTH"]:
                if insurance_rate:
                    if part["data_key"].part_no in ["RECAL STATIC", "RECAL-RTL-STATIC"]:
                        row_data.update({ part["data_key"].qbo_product_service: round(float(insurance_rate.static), 2) })
                        row_data.update({ "Glass:Labor": round(float(row_data["Labor"]) - float(insurance_rate.static), 2) })
                    elif part["data_key"].part_no in ["RECAL DYNAMIC", "RECAL-RTL-DYNAMIC"]:
                        row_data.update({ part["data_key"].qbo_product_service: round(float(insurance_rate.dynamic), 2) })
                        row_data.update({ "Glass:Labor": round(float(row_data["Labor"]) - float(insurance_rate.dynamic), 2) })
                    elif part["data_key"].part_no in ["RECAL DUALMETHOD", "RECAL-RTL-BOTH"]:
                        row_data.update({ part["data_key"].qbo_product_service: round(float(insurance_rate.dual), 2) })
                        row_data.update({ "Glass:Labor": round(float(row_data["Labor"]) - float(insurance_rate.dual), 2) })
                else:
                    if row_data["Labor"] == 0:
                        row_data.update({ 
                            "Glass:Labor": row_data["Labor"],
                            material_field: float(row_data["Materials"]) - 250,
                            "ADAS:Static Recalibration": 250
                        })
                    else:
                        row_data.update({ 
                            "Glass:Labor": float(row_data["Labor"]) - 250,
                            "ADAS:Static Recalibration": 250
                        })
        
        for part in row_data["Parts"]:
            if part.get("data_key", None) == None:
                continue
            if part["data_key"].part_no == "R&I":
                row_data.update({
                    "Glass:R&I": float(row_data["Labor"]),
                    "Glass:Labor": None
                })
                
        cus_name = f'{row_data["First Name"] if row_data["First Name"] else ""} {row_data["Last Name"] if row_data["Last Name"] else ""} {row_data["Commercial Account Name"] if row_data["Commercial Account Name"] else ""}'
        if bool(re.search(r'\(\d{3}\) \d{3}-\d{4}', cus_name)) or bool(re.search(r'\d{10}', cus_name)):
            row_data.update({ "Proper Name": "Customer" })
        else:
            row_data.update({ "Proper Name": cus_name.strip().title() })
        
        row_data.update({ "Parts": ", ".join([part["part_number"] for part in row_data["Parts"]]) })
        
        if row_data["Deductible"]:
            row_data.update({ "Insurance Discounts:Deductible": -round(float(row_data["Deductible"]), 2) })
        
        return row_data