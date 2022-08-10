from typing import Any

from fastapi import APIRouter, Depends
from app.core.settings.development import settings
from sqlalchemy.orm import Session
from app.api import dependencies
from app import schemas, models
from app.services import CRUD
router = APIRouter()

@router.post("/")
def create_product(
    *,
    db: Session = Depends(dependencies.get_db),
    producto: schemas.ProductoCreate
) -> Any:
    db_product = CRUD.producto.create(db=db, obj_in=producto)
    return db_product
