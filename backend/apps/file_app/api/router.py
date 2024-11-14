from fastapi import APIRouter

from backend.apps.file_app.api.v1.core import router as file_router

v1 = APIRouter()

v1.include_router(file_router)
