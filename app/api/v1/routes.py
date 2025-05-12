from fastapi import APIRouter
from app.api.v1.brief_routes import router as brief_router
from app.api.v1.health import router as health_router

router = APIRouter()
router.include_router(brief_router)
router.include_router(health_router)
