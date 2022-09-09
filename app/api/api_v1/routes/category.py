from typing import Any, List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from app.api.dependencies import db, jwt_bearer
from app import schemas
from app.services import crud
router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_category(
    *,
    db: Session = Depends(db.get_db),
    category: schemas.CategoryCreate,
    current_employee: schemas.Employee = Depends(
        jwt_bearer.get_current_active_employee),
) -> Any:
    """
    Endpoint to create a new category.

        params: category: CategoryCreate

        return: CategoryINDB

    """
    db_category = crud.categoria.create(db=db, obj_in=category)
    return db_category


@router.get("/", status_code=200)
def read_categories(
    *,
    db: Session = Depends(db.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Endpoint to read all categories.

        params: skip: int, limit: int

        return: List[CategoryINDB]

    """

    db_category = jsonable_encoder(
        crud.categoria.get_multi(db=db, skip=skip, limit=limit))
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'count': len(db_category),
        'next': f'http://localhost:8000/api/v1/category?skip={skip+limit}&limit={limit}',
        'previous': None if skip == 0 else f'http://localhost:8000/api/v1/category?skip={skip-limit}&limit={limit}',
        'results': db_category
    })


@router.get("/{category_id}", status_code=200)
def read_category(
    *,
    db: Session = Depends(db.get_db),
    category_id: int,
) -> Any:
    """
    Endpoint to read a category.

        params: category_id: int

        return: CategoryINDB

    """

    db_category = crud.categoria.get(db=db, id=category_id)

    if db_category is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
            'detail': 'Category not found'
        })

    return db_category


@router.put("/{category_id}", status_code=200)
def update_category(
    *,
    db: Session = Depends(db.get_db),
    category_id: int,
    current_employee: schemas.Employee = Depends(
        jwt_bearer.get_current_active_employee),
    category: schemas.CategoryUpdate
) -> Any:
    """
    Endpoint to update a category.

        params: category_id: int, category: CategoryUpdate

        return: CategoryINDB

    """

    db_obj = crud.categoria.get(db=db, id=category_id)

    if db_obj is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
            'detail': 'Not found'
        })
    db_category = crud.categoria.update(db=db, id=category_id, obj_in=category)
    return db_category


@router.delete("/{category_id}", status_code=200)
def delete_category(
    *,
    db: Session = Depends(db.get_db),
    category_id: int,
    current_employee: schemas.Employee = Depends(
        jwt_bearer.get_current_active_employee),
) -> Any:
    """
    Endpoint to delete a category.

        params: category_id: int

        return: CategoryINDB

    """

    db_obj = crud.categoria.get(db=db, id=category_id)

    if db_obj is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
            'detail': 'Not found'
        })
    db_category = crud.categoria.delete(db=db, id=category_id)
    return db_category


@router.get("/{category_id}/products", status_code=200)
def read_products(
    *,
    db: Session = Depends(db.get_db),
    category_id: int,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Endpoint to read all products of a category.

        params: category_id: int, skip: int, limit: int

        return: List[ProductoINDB]

    """

    db_product = jsonable_encoder(crud.producto.get_multi_by_category(
        db=db, skip=skip, limit=limit, category_id=category_id))
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'count': len(db_product),
        'next': f'http://localhost:8000/api/v1/category/{category_id}/products?skip={skip+limit}&limit={limit}',
        'previous': None if skip == 0 else f'http://localhost:8000/api/v1/category/{category_id}/products?skip={skip-limit}&limit={limit}',
        'results': db_product
    })
