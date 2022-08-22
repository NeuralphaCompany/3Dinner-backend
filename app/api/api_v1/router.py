from fastapi import APIRouter

from app.api.api_v1.routes import product
from app.api.api_v1.routes import category
from app.api.api_v1.routes import user
from app.api.api_v1.routes import employee
from app.api.api_v1.routes import login

api_route = APIRouter()
api_route.include_router(product.router, prefix="/product", tags=["product"])
api_route.include_router(category.router, prefix="/category", tags=["category"])
api_route.include_router(user.router, prefix="/user", tags=["user"])
api_route.include_router(employee.router, prefix="/employee", tags=["employee"])
api_route.include_router(login.router, prefix="/login", tags=["login"])