from fastapi import APIRouter

health_router = APIRouter(prefix="/health")

@health_router.get("/")
def health_check():
    return { "message": "running!" }

__all__ = ["health_router"]


