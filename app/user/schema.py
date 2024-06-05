import datetime
from typing import Optional
from pydantic import EmailStr
from pydantic import BaseModel

class UserBase(BaseModel):
    email: Optional[EmailStr]
    full_name: Optional[str]
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str]
    google_id: Optional[str] = None
    updated_at: Optional[str] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    created_at: Optional[str] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    email_verified: Optional[bool] = False
    role: Optional[int] = 2 # 1-Admin 2-User
    avatar_url: Optional[str] = "static/avatar.png"
    forgot_password_token: Optional[str] = None
    activated: Optional[bool] = True
    
class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserSignUp(UserBase):
    pass
class UserLogin(BaseModel):
    email: str
    password: str