from fastapi import APIRouter, Depends

router = APIRouter()

@router.post("/")
def Hola():
    return {"message": "Hola"}