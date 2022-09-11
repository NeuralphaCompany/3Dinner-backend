from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

from app import schemas
from app.services import crud
from app.core.config import get_app_settings

from app.services.db import session, base

settings = get_app_settings()

def init_db(db:Session) -> None:
    base.Base.metadata.create_all(bind=session.engine)

    employee = crud.employee.get_by_email(db, email=settings.first_superemployee_email)
    if not employee:
        employee_in = schemas.EmployeeCreate(
            email = settings.first_superemployee_email,
            is_active = True,
            is_superuser = True,
            name = settings.first_superemployee_name,
            password = settings.first_superemployee_password,
            rol = 0
        )
        employee = crud.employee.create(db, obj_in=employee_in)
    
    user = crud.user.get(db, id=1)
    if not user:
        user_in = schemas.UserCreate(
            email = settings.first_superemployee_email,
            is_active = True,
            name = settings.first_superemployee_name,
        )
        user = crud.user.create(db, obj_in=user_in)