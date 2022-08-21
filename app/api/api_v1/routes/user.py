from typing import Any, List

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from app.api.api_v1.dependencies import db

from app import schemas
from app.services import crud
router = APIRouter()

@router.post("/",
    status_code = 201,
)
def create_user(
    *,
    db: Session = Depends(db.get_db),
    user: schemas.UserCreate
) -> Any:
    """
    Endpoint to create a new user.
    
        params: user: UserCreate
    
        return: UserINDB
    
    """
    db_user = crud.user.create(db=db, obj_in=user)
    return db_user

@router.get('/', status_code = 200)
def read_users(
    *,
    db: Session = Depends(db.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Endpoint to read all users.
    
        params: skip: int, limit: int
    
        return: List[UserINDB]
    
    """

    db_user = jsonable_encoder(crud.user.get_multi(db=db, skip=skip, limit=limit))
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'count': len(db_user),
        'next': f'http://localhost:8000/api/v1/user?skip={skip+limit}&limit={limit}',
        'previous': None if skip == 0 else f'http://localhost:8000/api/v1/user?skip={skip-limit}&limit={limit}',
        'results': db_user
    })

@router.get('/{user_id}', status_code = 200)
def read_user(
    *,
    db: Session = Depends(db.get_db),
    user_id: int,
) -> Any:
    """
    Endpoint to read a user.
    
        params: user_id: int
    
        return: UserINDB
    
    """

    db_user = crud.user.get(db=db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put('/{user_id}', status_code = 200)
def update_user(
    *,
    db: Session = Depends(db.get_db),
    user_id: int,
    user: schemas.UserUpdate,
) -> Any:
    """
    Endpoint to update a user.
    
        params: user_id: int, user: UserUpdate
    
        return: UserINDB
    
    """

    db_user = crud.user.get(db=db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user = crud.user.update(db=db, db_obj=db_user, obj_in=user)
    return db_user

@router.delete('/{user_id}', status_code = 200)
def delete_user(
    *,
    db: Session = Depends(db.get_db),
    user_id: int,
) -> Any:
    """
    Endpoint to delete a user.
    
        params: user_id: int
    
        return: UserINDB
    
    """

    db_user = crud.user.get(db=db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user = crud.user.remove(db=db, id=user_id)
    return db_user