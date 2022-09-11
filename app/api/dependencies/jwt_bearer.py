from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.schemas import employee

from app.services import crud
from app import models, schemas
from app.core import security
from app.core.config import get_app_settings
from app.services.db.session import SessionLocal
from .db import get_db

settings = get_app_settings()

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"http://localhost:8000{settings.api_prefix_v1}/login/access-token"
)


def get_current_employee(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.Employee:
    try:
        payload = jwt.decode(
            token, str(settings.secret_key), algorithms=[settings.algorithm]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    employee = crud.employee.get(db, id=token_data.sub)
    if not employee:
        raise HTTPException(status_code=404, detail="User not found")
    return employee


def get_current_active_employee(
    db: Session = Depends(get_db),
    current_employee: models.Employee = Depends(get_current_employee),
) -> models.Employee:
    if not crud.employee.is_active(db=db, user=current_employee):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_employee

def get_current_active_superemployee(
    db: Session = Depends(get_db),
    current_employee: models.Employee = Depends(get_current_active_employee)
) -> models.Employee:
    if not crud.employee.is_superuser(db= db, user=current_employee):
        return HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not a superuser")
    return current_employee
