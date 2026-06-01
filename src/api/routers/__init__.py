from fastapi import APIRouter
from .departures import departures_router
from .health import health_router

api = APIRouter(prefix="/api")

api.include_router(departures_router)
api.include_router(health_router)

__all__ = ["api"]
