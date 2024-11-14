from fastapi import APIRouter

from backend.common.conf import settings
from backend.apps.file_app.api.v1.core import router as file_router

route = APIRouter(prefix=settings.API_V1_STR)

route.include_router(file_router)
