from typing import Any, List

from fastapi import APIRouter, Depends, status, HTTPException, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from app.api.dependencies import db
from app import schemas
from app.services import crud

router = APIRouter()

@router.post("/",
    status_code = 201,
    response_model=schemas.Employee
)
def create_employee(
    *,
    db: Session = Depends(db.get_db),
    employee: schemas.EmployeeCreate
) -> schemas.Employee:
    """
    Endpoint to create a new employee.

        params: employee: EmployeeCreate
    """
    db_employee = crud.employee.create(db=db, obj_in=employee)
    return db_employee

@router.get("/", status_code = 200)
def read_employees(
    *,
    db: Session = Depends(db.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Endpoint to read all employees.

        params: skip: int, limit: int
    """

    db_employee = jsonable_encoder(crud.employee.get_multi(db=db, skip=skip, limit=limit))
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'count': len(db_employee),
        'next': f'http://localhost:8000/api/v1/employee?skip={skip+limit}&limit={limit}',
        'previous': None if skip == 0 else f'http://localhost:8000/api/v1/employee?skip={skip-limit}&limit={limit}',
        'results': db_employee
    })

@router.get("/{id}", status_code = 200)
def read_employee(
    *,
    db: Session = Depends(db.get_db),
    id: int,
) -> Any:
    """
    Endpoint to read an employee.

        params: id: int
    """

    db_employee = crud.employee.get(db=db, id=id)
    return db_employee

@router.put("/me", status_code = 200)
def update_employee(
    *,
    db: Session = Depends(db.get_db),
    password : str = Body(None),
    name : str = Body(None),
    email : str = Body(None),
    cellphone : str = Body(None),
) -> Any:
    """
    Endpoint to update an employee.
    """
    if password is not None:
        return "Works!"

    

@router.delete("/{id}", status_code = 200)
def delete_employee(
    *,
    db: Session = Depends(db.get_db),
    id: int,
) -> Any:
    """
    Endpoint to delete an employee.

        params: id: int
    """

    db_obj = crud.employee.get(db=db, id=id)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db_employee = crud.employee.delete(db=db, id=id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'detail': 'Employee deleted'
    })