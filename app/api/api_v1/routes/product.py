from typing import Any, List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from app.api.api_v1.dependencies import dependencies
from app import schemas
from app.services import CRUD
router = APIRouter()

@router.post("/",
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    *,
    db: Session = Depends(dependencies.get_db),
    producto: schemas.ProductoCreate
) -> Any:
    """
    Endpoint to create a new product.

        params: product: ProductoCreate

        return: ProductoINDB

    """
    db_product = CRUD.producto.create(db=db, obj_in=producto)
    return db_product


@router.get("/", status_code = 200)
def read_products(
    *,
    db: Session = Depends(dependencies.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Endpoint to read all products.

        params: skip: int, limit: int

        return: List[ProductoINDB]

    """

    db_product = jsonable_encoder(CRUD.producto.get_multi(db=db, skip=skip, limit=limit))
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'count': len(db_product),
        'next': f'http://localhost:8000/api/v1/product?skip={skip+limit}&limit={limit}',
        'previous': None if skip == 0 else f'http://localhost:8000/api/v1/product?skip={skip-limit}&limit={limit}',
        'results': db_product
    })


@router.get("/{product_id}", status_code = 200)
def read_product(
    *,
    db: Session = Depends(dependencies.get_db),
    product_id: int,
) -> Any:
    """
    Endpoint to read a product.

        params: product_id: int

        return: ProductoINDB

    """

    db_product = CRUD.producto.get(db=db, id=product_id)
    return db_product


@router.put("/{product_id}", status_code = 200)
def update_product(
    *,
    db: Session = Depends(dependencies.get_db),
    product_id: int,
    producto: schemas.ProductoUpdate,
) -> Any:
    """
    Endpoint to update a product.

        params: product_id: int, producto: ProductoUpdate

        return: ProductoINDB updated

    """

    db_obj = CRUD.producto.get(db=db, id=product_id)

    if db_obj is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
            'detail': 'Product not found'
        })
    else:
        db_product = CRUD.producto.update(db=db, db_obj=CRUD.producto.get(db=db, id=product_id), obj_in=producto)
        return db_product


@router.delete("/{id}")
def delete_product(
    *,
    db: Session = Depends(dependencies.get_db),
    id: int
) -> Any:
    """
    Endpoint to delete a product.

        params: id: int

        return: JSONResponse with status_code=status.HTTP_204_NO_CONTENT if success, status_code=status.HTTP_404_NOT_FOUND if not found product  

    """
    db_product = CRUD.producto.get(db=db, id=id)
    if db_product:
        CRUD.producto.delete(db=db, id=id)
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={
        "code": status.HTTP_204_NO_CONTENT,
        "message": "Producto eliminado",
        "object": jsonable_encoder(db_product)
    })
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Producto no encontrado",
            "object": None
        })
    


