from typing import Optional

from pydantic import BaseModel, EmailStr, root_validator, SecretStr
from datetime import datetime

from app.schemas.multi_response import multi_response

class EmployeeBase(BaseModel):
    email: Optional[EmailStr]
    is_active: Optional[bool] =True
    name: str
    cellphone: Optional[str]
    created_at: Optional[datetime]
    rol: int
    is_superuser: bool = False

class EmployeeCreate(EmployeeBase):
    @root_validator()
    def check_email_or_cellphone(cls, values: dict):
        if (values['email'] is None) and (values['cellphone'] is None):
            raise ValueError('Email or cellphone is required')
        return values
    password: str

class EmployeeUpdate(EmployeeBase):
    password : Optional[str] = None

class EmployeeInDBBase(EmployeeBase):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class Employee(EmployeeInDBBase):
    pass

class EmployeeInDB(EmployeeInDBBase):
    hashed_password: SecretStr


class EmployeesResponse(multi_response[EmployeeInDB]):
    pass