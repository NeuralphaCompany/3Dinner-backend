from typing import Any, List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from app.api import dependencies
from app import schemas, models
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
    db_product = CRUD.producto.create(db=db, obj_in=producto)
    return db_product

@router.get("/", status_code = 200)
def read_product(
    *,
    db: Session = Depends(dependencies.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    db_product = jsonable_encoder(CRUD.producto.get_multi(db=db, skip=skip, limit=limit))
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'count': len(db_product),
        'next': f'http://localhost:8000/api/v1/product?skip={skip+limit}&limit={limit}',
        'previous': None if skip == 0 else f'http://localhost:8000/api/v1/product?skip={skip-limit}&limit={limit}',
        'results': db_product
    })

@router.delete("/{id}")
def delete_product(
    *,
    db: Session = Depends(dependencies.get_db),
    id: int
) -> Any:
    db_product = CRUD.producto.delete(db=db, id=id)
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={
        "code": status.HTTP_204_NO_CONTENT,
        "message": "Producto eliminado",
        "object": db_product
    })


