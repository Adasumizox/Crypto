from fastapi import APIRouter

from cryptoAPI.src.api.endpoints import asymmetric
from cryptoAPI.src.api.endpoints import symmetric

api_router = APIRouter()
api_router.include_router(symmetric.router, prefix="/symmetric", tags=["symmetric"])
api_router.include_router(asymmetric.router, prefix="/asymmetric", tags=["asymmetric"])
