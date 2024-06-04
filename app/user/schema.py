from typing import Optional
from pydantic import EmailStr
from pydantic import BaseModel

class UserBase(BaseModel):
    email: Optional[EmailStr]
    full_name: Optional[str]
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str]
    address: Optional[str] = None
    postal_code: Optional[str] = None
    province: Optional[str] = None
    pays: Optional[str] = None
    phone: Optional[str] = None
    google_id: Optional[str] = None
    updated_at: Optional[str] = None
    created_at: Optional[str] = None
    email_verified: Optional[bool] = None
    role: Optional[int] = 2 # 1-Admin 2-User
    avatar_url: Optional[str] = "static/avatar.png"
    user_type: Optional[str] = "Particulier"
    forgot_password_token: Optional[str] = None
    activated: Optional[bool] = True
    
class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserLogin(BaseModel):
    email: str
    password: str