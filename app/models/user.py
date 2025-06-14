from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

class UserRegister(BaseModel):
    name : str
    email: EmailStr
    password : str
    confirm_password : str
    is_admin: Optional[bool] = False
    created_at : Optional[datetime] = datetime.now()
    updated_at : Optional[datetime] = datetime.now()

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    password : str 
    is_admin: Optional[bool] = False

class UserLogin(BaseModel):
    email: str
    password : str


class UserUpdate(BaseModel):
    name: Optional[str] =None
    email: Optional[EmailStr]= None

class ChangePassword(BaseModel):
    old_password: str
    password : str
    confirm_password : str
