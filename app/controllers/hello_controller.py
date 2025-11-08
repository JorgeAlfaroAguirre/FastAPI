from fastapi import APIRouter

router = APIRouter(prefix="/miapp", tags=["Hello"])

@router.get("")
def hola_mundo():
    return {"message": "hola mundo"}    