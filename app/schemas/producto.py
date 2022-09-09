from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.multi_response import multi_response


class ProductoCreate(BaseModel):
    name: str = Field(
        ...,
        description="Nombre del producto",
        example="Producto 1",
        min_length=1,
        max_length=255,
    )
    description: str = Field(
        ...,
        description="Descripción del producto",
        example="Descripción del producto 1",
        min_length=1,
        max_length=300,
    )
    short_description: Optional[str] = Field(
        description="Descripción corta del producto",
        example="Descripción corta del producto 1",
        min_length=1,
        max_length=150,
    )
    price: int = Field(
        ...,
        description="Precio del producto con IVA incluído",
        example=100,
        gt=0,
    )
    image: Optional[str] = Field(
        description="Imagen del producto",
        example="http://localhost:8000/images/producto1.jpg",
        min_length=1,
        max_length=1000,
    )
    image_galery: Optional[List[str]] = Field(
        description="Imagenes del producto",
        example=["http://localhost:8000/images/producto1.jpg",
                 "http://localhost:8000/images/producto2.jpg"],
        min_items=1,
        max_items=10,
    )
    ingredients: Optional[List[str]] = Field(
        description="Ingredientes del producto",
        example=["Ingrediente 1", "Ingrediente 2"],
        min_items=1,
        max_items=10,
    )
    category_id: int = Field(
        ...,
        description="ID de la categoría del producto",
        example=1,
        gt=0,
    )
    baseIva: Optional[int] = 0
    adiciones: Optional[List[int]] or List[str]



class ProductoUpdate(ProductoCreate):
    pass


class ProductoInDBBase(ProductoCreate):
    id: int

    class config:
        orm_mode = True


class Producto(ProductoInDBBase):
    pass


class ProductsResponse(multi_response[ProductoInDBBase]):
    pass
