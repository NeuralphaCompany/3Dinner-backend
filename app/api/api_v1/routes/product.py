
from typing import Any, List

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from app.api.dependencies import db
from app import models, schemas
from app.services import crud
from app.api.dependencies import jwt_bearer

router = APIRouter()

@router.post("/",
    status_code = 201,
)
def create_product(
    *,
    db: Session = Depends(db.get_db),
    current_employee: models.Employee= Depends(jwt_bearer.get_current_active_employee),
    producto: schemas.ProductoCreate
) -> Any:
    """
    Endpoint to create a new product.

        params: product: ProductoCreate

        return: ProductoINDB

    """
    db_product = crud.producto.create(db=db, obj_in=producto)
    return db_product


@router.get("/", status_code = 200)
def read_products(
    *,
    db: Session = Depends(db.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Endpoint to read all products.

        params: skip: int, limit: int

        return: List[ProductoINDB]

    """

    db_product = jsonable_encoder(crud.producto.get_multi(db=db, skip=skip, limit=limit))
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'count': len(db_product),
        'next': f'http://localhost:8000/api/v1/product?skip={skip+limit}&limit={limit}',
        'previous': None if skip == 0 else f'http://localhost:8000/api/v1/product?skip={skip-limit}&limit={limit}',
        'results': db_product
    })


@router.get("/{product_id}", status_code = 200)
def read_product(
    *,
    db: Session = Depends(db.get_db),
    product_id: int,
) -> Any:
    """
    Endpoint to read a product.

        params: product_id: int

        return: ProductoINDB

    """

    db_product = crud.producto.get(db=db, id=product_id)
    return db_product


@router.put("/{product_id}", status_code = 200)
def update_product(
    *,
    db: Session = Depends(db.get_db),
    product_id: int,
    producto: schemas.ProductoUpdate,
) -> Any:
    """
    Endpoint to update a product.

        params: product_id: int, producto: ProductoUpdate

        return: ProductoINDB updated

    """

    db_obj = crud.producto.get(db=db, id=product_id)

    if db_obj is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
            'detail': 'Product not found'
        })
    else:
        db_product = crud.producto.update(db=db, db_obj=db_obj, obj_in=producto)
        return db_product


@router.delete("/{id}", status_code = status.HTTP_200_OK)
def delete_product(
    *,
    db: Session = Depends(db.get_db),
    id: int,

) -> Any:
    """
    Endpoint to delete a product.

        params: id: int

        return: JSONResponse with status_code=status.HTTP_204_NO_CONTENT if success, status_code=status.HTTP_404_NOT_FOUND if not found product  

    """
    db_product = crud.producto.get(db=db, id=id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    db_product = crud.producto.delete(db=db, id=id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'detail': 'Product deleted'
    })
        
    