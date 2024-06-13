import smtplib
import zipfile

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from decouple import config
from sqlalchemy.orm import Session

from fastapi import Request

from app.auth.auth_handler import decodeJWT

# SMTP server details
smtp_server = "mail.gandi.net"
smtp_port = 587
smtp_username = "register@reeact.io"
smtp_password = "register@reeact.io"
sender_email = "register@reeact.io"

def get_user_id(request: Request):
    bearer_token = request.headers["Authorization"]
    jwt_token = bearer_token[7:]
    payload = decodeJWT(jwt_token)
    user_id = payload.get("user_id")
    return user_id

def check_user_role(request: Request):
    bearer_token = request.headers["Authorization"]
    jwt_token = bearer_token[7:]
    payload = decodeJWT(jwt_token)
    user_role = payload.get("user_role")
    if user_role == 0 or user_role == 1:
        return "Admin"
    elif user_role == 2:
        return "Customer"
    
def check_file_type(filename):
    allowed_extensions = ['jpg', 'jpeg', 'png', 'pdf']  # Add more allowed extensions if needed
    file_extension = filename.rsplit('.', 1)[-1].lower()
    if file_extension in allowed_extensions:
        return True
    else:
        return False

async def get_nested_value(d, key):
        keys = key.split(".")
        value = d
        for k in keys:
            value = value.get(k)
            if value is None:
                return None
        return value

def zip_files(file_paths, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for file in file_paths:
            zipf.write(file)
            
async def send_email(email: str, subject: str, email_body: str):    
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = subject
    
    msg.attach(MIMEText(email_body, "html"))
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print("Error sending email:", str(e))
        return False