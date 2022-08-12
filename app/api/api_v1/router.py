from fastapi import APIRouter

from app.api.api_v1.routes import product
from app.api.api_v1.routes import category

api_route = APIRouter()
api_route.include_router(product.router, prefix="/product", tags=["product"])
api_route.include_router(category.router, prefix="/category", tags=["category"])