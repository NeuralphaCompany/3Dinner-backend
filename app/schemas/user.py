from dataclasses import Field
from datetime import datetime
from pydantic import BaseModel, EmailStr, root_validator
from typing import Optional

class UserBase(BaseModel):
    email: Optional[EmailStr] 
    is_active: Optional[bool]
    name: str 
    cellphone: Optional[str] 
    created_at: Optional[datetime]

class UserCreate(UserBase):
    @root_validator()
    def check_email_or_cellphone(cls, values: dict):
        if (values['email'] is None) and (values['cellphone'] is None):
            raise ValueError('Email or cellphone is required')
        return values

class UserUpdate(UserBase):
    pass

class UserInDB(UserBase):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class User(UserInDB):
    pass
