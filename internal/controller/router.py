from fastapi import APIRouter

from controller import v1

api_router = APIRouter()
api_router.include_router(v1.router, prefix='/v1')

