from typing import Optional

from pydantic import BaseModel, Field

class CategoryCreate(BaseModel):
    name: str = Field(..., description="Nombre de la categoría", example="Categoría 1", min_length=1, max_length=255)
    image: Optional[str] = Field(description="Imagen de la categoría", example="http://localhost:8000/images/categoria1.jpg", min_length=1, max_length=1000)

class CategoryUpdate(CategoryCreate):
    pass

class CategoryInDBBase(CategoryCreate):
    id: int = Field(..., description="ID de la categoría", example=1, gt=0)
    class Config:
        orm_mode = True
