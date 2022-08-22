from typing import Any, Dict, Union
from sqlalchemy.orm import Session


from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.models.employee import Employee
from app.core.security import get_password_hash, check_password
from app.services.crud.base import CRUDBase



class CRUDEmployee(CRUDBase[Employee, EmployeeCreate, EmployeeUpdate]):
    def get_by_email(
        self, db: Session, email: str
    ) -> Employee:
        return db.query(Employee).filter(Employee.email == email).first()
    
    def get_by_cellphone(
        self, db: Session, cellphone: str
    ) -> Employee:
        return db.query(Employee).filter(Employee.cellphone == cellphone).first()
    
    def create(
        self, db: Session, obj_in: EmployeeCreate
    ) -> Employee:
        hashed_password = get_password_hash(obj_in.password)
        db_obj = Employee(
            name=obj_in.name,
            email=obj_in.email,
            cellphone=obj_in.cellphone,
            rol=obj_in.rol,
            is_superuser=obj_in.is_superuser,
            is_active=obj_in.is_active,
            hashed_password=hashed_password,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self, db: Session, *, obj_in: Union[EmployeeUpdate, Dict[str, Any]]
    ) -> Employee:
        if isinstance(obj_in, dict):
            update_date = obj_in
        else:
            update_date = obj_in.dict(exclude_unset=True)
        if update_date['password']:
            hashed_password = get_password_hash(update_date['password'])
            del update_date['password']
            update_date['hashed_password'] = hashed_password
        return super().update(db, obj_in=update_date)

    def authenticate(
        self, db: Session, *, email: str = None, cellphone: str = None, password: str
    ) -> Employee:
        user = self.get_by_email(db, email=email) or self.get_by_cellphone(db, cellphone=cellphone)
        if not user:
            raise Exception('User not found')
        if not user.is_active:
            raise Exception('User not active')
        if not check_password(password, user.hashed_password):
            raise Exception('Invalid password')
        return user

    def is_active(self, db: Session, *, user: Employee) -> bool:
        return user.is_active

    

employee = CRUDEmployee(Employee)