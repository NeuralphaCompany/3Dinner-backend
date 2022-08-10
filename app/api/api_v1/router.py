from fastapi import APIRouter

from app.api.api_v1.routes import product

api_route = APIRouter()
api_route.include_router(product.router, prefix="/product", tags=["product"])