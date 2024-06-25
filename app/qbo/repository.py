import json
import json
import logging
import datetime
import re

from sqlalchemy import extract, or_, and_
from sqlalchemy.orm import Session
from . import model, schema

from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from intuitlib.exceptions import AuthClientError

from quickbooks import QuickBooks
from quickbooks.objects import Customer, \
                                Account, \
                                Invoice, \
                                SalesReceipt, \
                                Payment, \
                                PaymentMethod, \
                                Item, \
                                SalesItemLine, \
                                SalesItemLineDetail, \
                                PaymentLine
from quickbooks.exceptions import AuthorizationException

class QBOController:
    def __init__(self,
                 client_id=None,
                 client_secret=None,
                 redirect_uri=None,
                 access_token=None,
                 refresh_token=None,
                 state_token=None,
                 id_token=None,
                 realm_id=None,
                 auth_code=None,
                 environment=None):

        self.client_id = client_id
        self.client_secret = client_secret
        self.environment = environment
        self.redirect_uri = redirect_uri

        self.access_token = access_token if access_token else "unknown"
        self.refresh_token = refresh_token if refresh_token else "unknown"
        self.state_token = state_token if state_token else "GlasscleanerOAuth"
        self.id_token = id_token
        self.realm_id = realm_id
        self.auth_code = auth_code
        
    async def init(self):
        self.auth_client = AuthClient(
            client_id=self.client_id,
            client_secret=self.client_secret,
            access_token=self.access_token,
            refresh_token=self.refresh_token,
            environment=self.environment,
            redirect_uri=self.redirect_uri
        )
        
        self.qb_client = QuickBooks(
            auth_client=self.auth_client,
            access_token=self.auth_client.access_token,
            refresh_token=self.auth_client.refresh_token,
            company_id=self.realm_id,
            sandbox=True if self.environment == 'sandbox' else False
        )
    
    async def get_authUri(self) -> str:
        """
        Returns the authorization URI for the QuickBooks Online API.

        Returns:
            str: The authorization URI.
        """

        return self.auth_client.get_authorization_url(
            scopes=[Scopes.ACCOUNTING],
            state_token=self.state_token
        )

    async def create_sales_receipt(self, payment_group_data, billing_data, insurance_companies, payment_method_to_account) -> SalesReceipt:
        """
        Creates a new QuickBooks Online sales receipt for a given payment group and billing data.
        
        Args:
            payment_group_data (dict): A dictionary containing payment group data, including the date and payment method.
            billing_data (dict): A dictionary containing billing data, including the customer name, job number, referral number, and VIN.
            payment_method_to_account (dict): A dictionary mapping payment method names to account names.
        
        Returns:
            SalesReceipt: The newly created QuickBooks Online sales receipt.
        """
        try:
            company_name = billing_data["Proper Name"]
            company_name = company_name.strip()
            company_name = " ".join(word.capitalize() for word in company_name.split(" "))
            company_name = company_name if insurance_companies.get(billing_data["Trading Partner"], None) == None else insurance_companies.get(billing_data["Trading Partner"], None)
            customer_list = Customer.filter(DisplayName=company_name if insurance_companies.get(billing_data["Trading Partner"], None) == None else insurance_companies.get(billing_data["Trading Partner"], None), qb=self.qb_client)
            
            if len(customer_list) > 0:
                new_customer = customer_list[0]
            else:
                new_customer = Customer()
                new_customer.CompanyName = company_name
                new_customer.DisplayName = company_name
                new_customer.ShipAddr = None
                new_customer.save(qb=self.qb_client)

            new_sales_receipt = SalesReceipt()
            new_sales_receipt.CustomerRef = new_customer.to_ref()
            new_sales_receipt.DocNumber = billing_data["Job #"][1:]
            new_sales_receipt.CustomField = [
                {
                    "DefinitionId": "1",
                    "Name": "Insurance Company",
                    "Type": "StringType",
                    "StringValue": company_name if billing_data["Trading Partner"] == "safelite" else ""
                },
                {
                    "DefinitionId": "2",
                    "Name": "Referral #",
                    "Type": "StringType",
                    "StringValue": billing_data["Referral #"][1:]
                },
                {
                    "DefinitionId": "3",
                    "Name": "Vin #",
                    "Type": "StringType",
                    "StringValue": billing_data["Vin #"][1:]
                }
            ]
            for key, value in billing_data.items():
                try:
                    value = float(value)
                    if value == float(0):
                        continue
                    new_item = Item().filter(FullyQualifiedName=key, qb=self.qb_client)
                    if len(new_item) > 0:
                        new_item = new_item[0]
                    else:
                        new_item = Item()
                        new_item.Name = key
                        new_item.Type = "Service"
                        new_item.FullyQualifiedName = key
                        new_item.IncomeAccountRef = {
                            "value": 5,
                            "name": "Sales"
                        }
                        new_item = new_item.save(qb=self.qb_client)
                    
                    if key == "Insurance Discounts:Deductible" and value > 0:
                        new_sales_receipt.DocNumber = f'{billing_data["Job #"][1:]}-1'
                     
                    line_item = SalesItemLine()
                    line_item.Amount = value
                    line_item.SalesItemLineDetail = SalesItemLineDetail()
                    line_item.SalesItemLineDetail.ItemRef = new_item.to_ref()
                    line_item.SalesItemLineDetail.Qty = 1
                    line_item.SalesItemLineDetail.UnitPrice = value
                    line_item.SalesItemLineDetail.ServiceDate = None
                    
                    try:
                        if key in ["Glass:Windshield Replacement", "Glass:Backglass Replacement", "Glass:Side window Replacement", "Glass:Quarter glass Replacement"]:
                            line_item.Description = f'{billing_data["Year"][1:]} {billing_data["Make"]} {billing_data["Model"]}'
                        else:
                            line_item.Description = None
                    except:
                        line_item.Description = None
                    new_sales_receipt.Line.append(line_item)
                except Exception as e:
                    continue

            payment_method = PaymentMethod.filter(Name=payment_group_data["x_action_type"], qb=self.qb_client)
            payment_method = payment_method[0] if len(payment_method) > 0 else None
            
            deposit_to_account = Account.filter(Name=payment_method_to_account[payment_group_data["x_action_type"]], qb=self.qb_client)
            deposit_to_account = deposit_to_account[0] if len(deposit_to_account) > 0 else None
            
            new_sales_receipt.PaymentMethodRef = payment_method.to_ref() if payment_method else None
            new_sales_receipt.DepositToAccountRef = deposit_to_account.to_ref() if deposit_to_account else None

            new_sales_receipt.TxnDate = payment_group_data["date"]
            new_sales_receipt.PrivateNote = f"https://uat.glassbiller.com/jobs/{billing_data['Job #'][1:]}"
            new_sales_receipt.ShipAddr = None
            new_sales_receipt.save(qb=self.qb_client)
            print(f"QBO Controller: New Sales Receipt Created - {billing_data['Job #'][1:]}")
            logging.info(f"QBO Controller: New Sales Receipt Created - {billing_data['Job #'][1:]}")
            return new_sales_receipt
        except AuthorizationException as authexception:
            if "Token expired" in authexception.detail:
                self.auth_client.refresh(self.refresh_token)
            print(f"QBO Controller: Faild Creating Sale receipt: {authexception}")
            logging.exception(authexception)
            raise authexception
        except Exception as e:
            print(print(f"QBO Controller: Faild Creating Sale receipt: {e}"))
            logging.exception(e)
            raise e

    async def create_invoice(self, payment_group_data, billing_data, customer=None) -> Invoice:
        try:
            company_name = ""
            if customer == None:
                company_name = billing_data["Proper Name"]
                company_name = company_name.strip()
                company_name = " ".join(word.capitalize() for word in company_name.split(" "))
                customer_list = Customer.filter(DisplayName=company_name if billing_data["Trading Partner"] != "safelite" else "Safelite Solutions Network", qb=self.qb_client)
                
                if len(customer_list) > 0:
                    customer = customer_list[0]
                else:
                    customer = Customer()
                    customer.CompanyName = company_name
                    customer.DisplayName = company_name
                    customer.ShipAddr = None
                    customer.save(qb=self.qb_client)
            
            new_invoice = Invoice()
            new_invoice.CustomerRef = customer.to_ref()
            new_invoice.DocNumber = billing_data["Job #"][1:]
            new_invoice.DueDate = payment_group_data["date"]
            new_invoice.TxnDate = payment_group_data["date"]
            
            new_invoice.CustomField = [
                {
                    "DefinitionId": "1",
                    "Name": "Insurance Company",
                    "Type": "StringType",
                    "StringValue": company_name if billing_data["Trading Partner"] == "safelite" else ""
                },
                {
                    "DefinitionId": "2",
                    "Name": "Referral #",
                    "Type": "StringType",
                    "StringValue": billing_data["Referral #"][1:]
                },
                {
                    "DefinitionId": "3",
                    "Name": "Vin #",
                    "Type": "StringType",
                    "StringValue": billing_data["Vin #"][1:]
                }
            ]
            
            total_amount = 0
            for key, value in billing_data.items():
                try:
                    value = float(value)
                    if value == float(0):
                        continue
                    
                    new_item = Item().filter(FullyQualifiedName=key, qb=self.qb_client)
                    if len(new_item) > 0:
                        new_item = new_item[0]
                    else:
                        new_item = Item()
                        new_item.Name = key
                        new_item.Type = "Service"
                        new_item.FullyQualifiedName = key
                        new_item.IncomeAccountRef = {
                            "value": 5,
                            "name": "Sales"
                        }
                        new_item = new_item.save(qb=self.qb_client)

                    line_item = SalesItemLine()
                    line_item.Amount = value
                    line_item.SalesItemLineDetail = SalesItemLineDetail()
                    line_item.SalesItemLineDetail.ItemRef = new_item.to_ref()
                    line_item.SalesItemLineDetail.Qty = 1
                    line_item.SalesItemLineDetail.UnitPrice = value
                    line_item.SalesItemLineDetail.ServiceDate = None
                    try:
                        if key in ["Glass:Windshield Replacement", "Glass:Backglass Replacement", "Glass:Side window Replacement", "Glass:Quarter glass Replacement"]:
                            line_item.Description = f'{billing_data["Year"][1:]} {billing_data["Make"]} {billing_data["Model"]}'
                        else:
                            line_item.Description = None
                    except:
                        line_item.Description = None
                    new_invoice.Line.append(line_item)
                    total_amount += value
                except Exception as e:
                    continue
            
            new_invoice.Balance = total_amount
            new_invoice.TotalAmt = total_amount
            new_invoice.PrivateNote = f"https://uat.glassbiller.com/jobs/{billing_data['Job #'][1:]}"
            new_invoice.save(qb=self.qb_client)
            print(f"QBO Controller: New Invoice Created - {billing_data['Job #'][1:]}")
            logging.info(f"QBO Controller: New Invoice Created - {billing_data['Job #'][1:]}")
            return new_invoice
        except AuthorizationException as authexception:
            if "Token expired" in authexception.detail:
                self.auth_client.refresh(self.refresh_token)
            print(f"QBO Controller: Faild Creating Invoice: {authexception}")
            logging.exception(authexception)
            raise authexception
        except Exception as e:
            print(f"QBO Controller: Faild Creating Invoice {e}")
            logging.exception(e)
            return None

    async def create_payment(self, payment_group_data, billing_data_list, insurance_companies, payment_method_to_account) -> Payment:
        try:
            company_name = billing_data_list[0]["Proper Name"]
            company_name = company_name.strip()
            company_name = " ".join(word.capitalize() for word in company_name.split(" "))
            customer_list = Customer.filter(DisplayName=company_name if insurance_companies.get(billing_data_list[0]["Trading Partner"], None) == None else insurance_companies.get(billing_data_list[0]["Trading Partner"], None), qb=self.qb_client)
            
            if len(customer_list) > 0:
                new_customer = customer_list[0]
            else:
                new_customer = Customer()
                new_customer.CompanyName = company_name
                new_customer.DisplayName = company_name
                new_customer.ShipAddr = None
                new_customer.save(qb=self.qb_client)
            
            new_payment = Payment()
            new_payment.CustomerRef = new_customer.to_ref()
            payments_list = {payment["job_id"]: payment for payment in payment_group_data["payments"]}
            for billing_data in billing_data_list:
                invoice_list = Invoice.filter(DocNumber=billing_data["Job #"][1:], qb=self.qb_client)
                if len(invoice_list) > 0:
                    new_invoice = invoice_list[0]
                else:
                    new_invoice = await self.create_invoice(payment_group_data, billing_data, new_customer)
                
                payment_line_item = PaymentLine()
                payment_line_item.Amount = float(payments_list[int(billing_data["Job #"][1:])]["amount"])
                payment_line_item.LinkedTxn.append(new_invoice.to_linked_txn())
                
                new_payment.Line.append(payment_line_item)

            payment_method = PaymentMethod.filter(Name=payment_group_data["x_action_type"], qb=self.qb_client)
            payment_method = payment_method[0] if len(payment_method) > 0 else None
            
            deposit_to_account = Account.filter(Name=payment_method_to_account[payment_group_data["x_action_type"]], qb=self.qb_client)
            deposit_to_account = deposit_to_account[0] if len(deposit_to_account) > 0 else None
            
            new_payment.PaymentMethodRef = payment_method.to_ref() if payment_method else None
            new_payment.DepositToAccountRef = deposit_to_account.to_ref() if deposit_to_account else None
            
            new_payment.TxnDate = payment_group_data["date"]
            new_payment.TotalAmt = payment_group_data["total_amount"]
            new_payment.save(qb=self.qb_client)
            print(f"QBO Controller: New Payment Created- {payment_group_data['payments'][0]['job_id']}")
            logging.info(f"QBO Controller: New Payment Created- {payment_group_data['payments'][0]['job_id']}")
            return new_payment
        except AuthorizationException as authexception:
            if "Token expired" in authexception.detail:
                self.auth_client.refresh(self.refresh_token)
            print(f"QBO Controller: Faild Creating Payment: {authexception}")
            logging.exception(authexception)
            raise authexception
        except Exception as e:
            print(f"QBO Controller: Faild Creating Payment {e}")
            logging.exception(e)
            return None

    async def check_invoice_paid(self, docnumber):
        try:
            invoice_list = Invoice.filter(DocNumber=docnumber, qb=self.qb_client)
            if len(invoice_list) > 0:
                invoice = invoice_list[0]
                if invoice.Balance == 0:
                    return True
            else:
                return False
        except AuthorizationException as authexception:
            if "Token expired" in authexception.detail:
                self.auth_client.refresh(self.refresh_token)
            print(f"QBO Controller: Faild Checking Invoice Paid: {authexception}")
            logging.exception(authexception)
            raise authexception
        except Exception as e:
            print(f"QBO Controller: Faild Checking Invoice Paid {e}")
            logging.exception(e)
            return False

class QboRepo:
    async def create_setting(setting_data: schema.QboSetting, db: Session):
        try:
            now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
            new_setting = model.QBSettings(
                user_id=setting_data.user_id,
                client_id=setting_data.client_id,
                client_secret=setting_data.client_secret,
                refresh_token=setting_data.refresh_token,
                access_token=setting_data.access_token,
                realm_id=setting_data.realm_id,
                created_at=now,
                updated_at=now
            )
            
            db.add(new_setting)
            db.commit()
            db.refresh(new_setting)
            return new_setting
        except Exception as e:
            db.rollback()
            print(f"QBO Repo: Failed Creating Setting {e}")
            logging.exception(e)
            return None
    
    async def update_setting(setting_data: dict, db: Session):
        try:
            now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
            setting = db.query(model.QBSettings).filter(model.QBSettings.id == setting_data["id"]).first()
            if setting:
                for key, value in setting_data.items():
                    if key == "id":
                        continue
                    setattr(setting, key, value)
                setattr(setting, "updated_at", now)
                db.commit()
                db.refresh(setting)
                return setting
            else:
                return None
        except Exception as e:
            db.rollback()
            print(f"QBO Repo: Failed Updating Setting {e}")
            logging.exception(e)
            return None
    
    async def get_setting_by_user_id(user_id: str, db: Session):
        try:
            setting = db.query(model.QBSettings).filter(model.QBSettings.user_id == user_id).first()
            return setting
        except Exception as e:
            print(f"QBO Repo: Failed Getting Setting {e}")
            logging.exception(e)
            return None