from fastapi import FastAPI
from app.api.api_v1.router import api_route


app = FastAPI()

app.include_router(api_route, prefix="/api/v1")

