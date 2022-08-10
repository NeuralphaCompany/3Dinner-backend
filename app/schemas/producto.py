from locale import strcoll
from pydantic import BaseModel


class ProductoCreate(BaseModel):
    nombre: str

class ProductoUpdate(ProductoCreate):
    pass

class ProductoInDBBase(BaseModel):
    id: int
    class config:
        orm_mode = True
    
