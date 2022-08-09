from fastapi import APIRouter

from app.api.api_v1.routes import item

api_route = APIRouter()
api_route.include_router(item.router, prefix="/item", tags=["item"])