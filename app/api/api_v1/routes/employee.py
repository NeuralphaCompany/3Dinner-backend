from typing import Any, List

from fastapi import APIRouter, Depends, status, HTTPException, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from app.api.dependencies import db, jwt_bearer
from app import schemas
from app.services import crud

router = APIRouter()


@router.post("/",
             status_code=201,
             response_model=schemas.Employee
             )
def create_employee(
    *,
    db: Session = Depends(db.get_db),
    super_employee: schemas.Employee = Depends(
        jwt_bearer.get_current_active_superemployee),
    employee: schemas.EmployeeCreate
) -> schemas.Employee:
    """
    Endpoint to create a new employee.

        params: employee: EmployeeCreate
    """
    db_employee = crud.employee.create(db=db, obj_in=employee)
    return db_employee


@router.get("/", status_code=200, response_model=List[schemas.Employee])
def read_employees(
    *,
    db: Session = Depends(db.get_db),
    super_employee: schemas.Employee = Depends(
        jwt_bearer.get_current_active_superemployee),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Endpoint to read all employees.

        params: skip: int, limit: int
    """

    db_employee = crud.employee.get_multi(db=db, skip=skip, limit=limit)
    return db_employee


@router.get("/{id}", status_code=200, response_model=schemas.Employee)
def read_employee(
    *,
    db: Session = Depends(db.get_db),
    current_employee: schemas.Employee = Depends(
        jwt_bearer.get_current_active_employee),
    id: int
) -> schemas.Employee:
    """
    Endpoint to read an employee.

        params: id: int
    """
    db_employee = crud.employee.get(db=db, id=id)
    if not (current_employee == db_employee or current_employee.is_superuser):
        return HTTPException(403, detail="You do not have permission to read this employee.")
    return db_employee


@router.put("/{id}", status_code=200, response_model=schemas.Employee)
def update_employee(
    *,
    db: Session = Depends(db.get_db),
    current_employee: schemas.Employee = Depends(
        jwt_bearer.get_current_active_superemployee),
    employee_in: schemas.EmployeeUpdate,
    id: int
) -> schemas.Employee:
    """
    Endpoint to update an employee.
    """
    employee = crud.employee.get(db=db, id=id)
    if not employee:
        return HTTPException(404, f"Employee with id {id} does not exist.")
    return crud.employee.update(db=db, obj_db=employee, obj_in=employee_in)


@router.delete("/{id}", status_code=200)
def delete_employee(
    *,
    db: Session = Depends(db.get_db),
    current_employee: schemas.Employee = Depends(
        jwt_bearer.get_current_active_employee),
    id: int
) -> Any:
    """
    Endpoint to delete an employee.

        params: id: int
    """

    db_obj = crud.employee.get(db=db, id=id)

    if db_obj is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    if not (current_employee == db_obj or current_employee.is_superuser):
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete an employee.")

    db_employee = crud.employee.delete(db=db, id=id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'detail': 'Employee deleted'
    })
