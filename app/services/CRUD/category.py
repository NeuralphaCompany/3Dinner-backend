
from app.services.CRUD.base import CRUDBase

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate

class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    pass

categoria = CRUDCategory(Category)