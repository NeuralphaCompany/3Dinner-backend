
from app.services.CRUD.base import CRUDBase

from app.models.producto import Producto
from app.schemas.producto import ProductoCreate, ProductoUpdate

class CRUDProducto(CRUDBase[Producto, ProductoCreate, ProductoUpdate]):
    pass

producto = CRUDProducto(Producto)